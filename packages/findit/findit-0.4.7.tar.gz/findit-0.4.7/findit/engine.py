import numpy as np
import typing
import cv2
import collections
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
from sklearn.cluster import KMeans

from findit.logger import logger
from findit import toolbox
from findit.toolbox import Point


class FindItEngine(object):
    def get_type(self):
        return self.__class__.__name__


class TemplateEngine(FindItEngine):
    """
    Default cv method is TM_CCORR_NORMED

    1. Opencv support only CV_TM_CCORR_NORMED & CV_TM_SQDIFF
        (https://stackoverflow.com/questions/35658323/python-opencv-matchtemplate-is-mask-feature-implemented)
    2. Personally I do not want to use SQDIFF series. Its max value is totally different from what we thought.
    """
    DEFAULT_CV_METHOD_NAME: str = 'cv2.TM_CCORR_NORMED'
    DEFAULT_SCALE: typing.Sequence = (1, 3, 10)
    DEFAULT_MULTI_TARGET_MAX_THRESHOLD: float = 0.99
    DEFAULT_MULTI_TARGET_DISTANCE_THRESHOLD: float = 10.0

    def __init__(self,
                 engine_template_cv_method_name: str = None,
                 engine_template_scale: typing.Sequence = None,
                 engine_template_multi_target_max_threshold: float = None,
                 engine_template_multi_target_distance_threshold: float = None,
                 *_, **__):
        """ eg: engine_template_cv_method_name -> cv_method_name """
        logger.info('engine {} preparing ...'.format(self.get_type()))

        # cv
        self.cv_method_name = engine_template_cv_method_name or self.DEFAULT_CV_METHOD_NAME
        self.cv_method_code = eval(self.cv_method_name)

        # scale
        self.scale = engine_template_scale or self.DEFAULT_SCALE

        # multi target max threshold ( max_val * max_threshold == real threshold )
        self.multi_target_max_threshold = engine_template_multi_target_max_threshold or self.DEFAULT_MULTI_TARGET_MAX_THRESHOLD
        self.multi_target_distance_threshold = engine_template_multi_target_distance_threshold or self.DEFAULT_MULTI_TARGET_DISTANCE_THRESHOLD

        logger.debug(f'cv method: {self.cv_method_name}')
        logger.debug(f'scale: {self.scale}')
        logger.debug(f'multi target max threshold: {self.multi_target_max_threshold}')
        logger.debug(f'multi target distance threshold: {self.multi_target_distance_threshold}')
        logger.info(f'engine {self.get_type()} loaded')

    def execute(self,
                template_object: np.ndarray,
                target_object: np.ndarray,
                mask_pic_object: np.ndarray = None,
                mask_pic_path: str = None,
                *_, **__) -> dict:
        # mask
        if (mask_pic_path is not None) or (mask_pic_object is not None):
            logger.info('mask detected')
            mask_pic_object = toolbox.pre_pic(mask_pic_path, mask_pic_object)

        # template matching
        min_val, max_val, min_loc, max_loc, point_list = self._compare_template(
            template_object,
            target_object,
            self.scale,
            mask_pic_object
        )

        # 'target_point' must existed
        return {
            'target_point': max_loc,
            'target_sim': max_val,
            'conf': {
                'engine_template_cv_method_name': self.cv_method_name,
                'engine_template_scale': self.scale,
                'engine_template_multi_target_max_threshold': self.multi_target_max_threshold,
                'engine_template_multi_target_distance_threshold': self.multi_target_distance_threshold
            },
            'raw': {
                'min_val': min_val,
                'max_val': max_val,
                'min_loc': min_loc,
                'max_loc': max_loc,
                'all': point_list,
            }
        }

    def _compare_template(self,
                          template_pic_object: np.ndarray,
                          target_pic_object: np.ndarray,
                          scale: typing.Sequence,
                          mask_pic_object: np.ndarray = None) -> typing.Sequence:
        """
        compare via template matching
        (https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/)

        :param template_pic_object:
        :param target_pic_object:
        :param scale: default to (1, 3, 10)
        :param mask_pic_object:
        :return: min_val, max_val, min_loc, max_loc
        """
        pic_height, pic_width = target_pic_object.shape[:2]
        result_list = list()

        for each_scale in np.linspace(*scale):
            # resize template
            resize_template_pic_object = toolbox.resize_pic_scale(template_pic_object, each_scale)

            # resize mask
            if mask_pic_object is not None:
                mask_pic_object = toolbox.resize_pic_scale(mask_pic_object, each_scale)

            # if template's size is larger than raw picture, break
            if resize_template_pic_object.shape[0] > pic_height or resize_template_pic_object.shape[1] > pic_width:
                break

            res = cv2.matchTemplate(
                target_pic_object,
                resize_template_pic_object,
                self.cv_method_code,
                mask=mask_pic_object)
            # each of current result is:
            # [(min_val, max_val, min_loc, max_loc), point_list, shape]

            current_result = [*self._parse_res(res), resize_template_pic_object.shape]
            result_list.append(current_result)

        logger.debug('scale search result: {}'.format(result_list))
        # get the best one
        loc_val, point_list, shape = sorted(result_list, key=lambda i: i[0][1])[-1]
        min_val, max_val, min_loc, max_loc = loc_val

        # fix position
        logger.debug('raw compare result: {}, {}, {}, {}'.format(min_val, max_val, min_loc, max_loc))
        min_loc, max_loc = map(lambda each_location: list(toolbox.fix_location(shape, each_location)),
                               [min_loc, max_loc])
        point_list = [list(toolbox.fix_location(shape, each))
                      for each in toolbox.point_list_filter(point_list, self.multi_target_distance_threshold)]
        logger.debug('fixed compare result: {}, {}, {}, {}'.format(min_val, max_val, min_loc, max_loc))

        return min_val, max_val, min_loc, max_loc, point_list

    def _parse_res(self, res: np.ndarray) -> typing.Sequence:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # multi target
        min_thresh = (max_val - 1e-6) * self.multi_target_max_threshold
        match_locations = np.where(res >= min_thresh)
        point_list = zip(match_locations[1], match_locations[0])

        # convert int32 to float
        point_list = [tuple(map(float, _)) for _ in point_list]

        return (min_val, max_val, min_loc, max_loc), point_list


class FeatureEngine(FindItEngine):
    # TODO need many sample pictures to test
    DEFAULT_CLUSTER_NUM: int = 3
    DEFAULT_DISTANCE_THRESHOLD: float = 0.75

    def __init__(self,
                 engine_feature_cluster_num: int = None,
                 engine_feature_distance_threshold: float = None,
                 *_, **__):
        logger.info('engine {} preparing ...'.format(self.get_type()))

        # for kmeans calculation
        self.cluster_num: int = engine_feature_cluster_num or self.DEFAULT_CLUSTER_NUM
        # for feature matching
        self.distance_threshold: float = engine_feature_distance_threshold or self.DEFAULT_DISTANCE_THRESHOLD

        logger.debug('cluster num: {}'.format(self.cluster_num))
        logger.debug('distance threshold: {}'.format(self.distance_threshold))
        logger.info('engine {} loaded'.format(self.get_type()))

    def execute(self,
                template_object: np.ndarray,
                target_object: np.ndarray,
                *_, **__) -> dict:
        point_list = self.get_feature_point_list(template_object, target_object)

        # no point found
        if not point_list:
            return {
                'target_point': (-1, -1),
                'raw': [],
            }

        center_point = self.calculate_center_point(point_list)

        readable_center_point = list(center_point)
        readable_point_list = [list(each) for each in point_list]

        return {
            'target_point': readable_center_point,
            'raw': readable_point_list,
            'conf': {
                'engine_feature_cluster_num': self.cluster_num,
                'engine_feature_distance_threshold': self.distance_threshold,
            },
        }

    def get_feature_point_list(self,
                               template_pic_object: np.ndarray,
                               target_pic_object: np.ndarray) -> typing.Sequence[Point]:
        """
        compare via feature matching

        :param template_pic_object:
        :param target_pic_object:
        :return:
        """
        # Initiate SURF detector
        surf = cv2.xfeatures2d.SURF_create()

        # find the keypoints and descriptors with SURF
        kp1, des1 = surf.detectAndCompute(template_pic_object, None)
        kp2, des2 = surf.detectAndCompute(target_pic_object, None)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # TODO here is a sample to show feature points
        # temp = cv2.drawMatchesKnn(template_pic_object, kp1, target_pic_object, kp2, matches, None, flags=2)
        # cv2.imshow('feature_points', temp)
        # cv2.waitKey(0)

        good = []
        if len(matches) == 1:
            good = [matches[0]]
        else:
            for m, n in matches:
                if m.distance < self.distance_threshold * n.distance:
                    good.append([m])

        point_list = list()
        for each in good:
            img2_idx = each[0].trainIdx
            each_point = Point(*kp2[img2_idx].pt)
            point_list.append(each_point)

        return point_list

    def calculate_center_point(self, point_list: typing.Sequence[Point]) -> Point:
        np_point_list = np.array(point_list)
        point_num = len(np_point_list)

        # if match points' count is less than clusters
        if point_num < self.cluster_num:
            cluster_num = 1
        else:
            cluster_num = self.cluster_num

        k_means = KMeans(n_clusters=cluster_num).fit(np_point_list)
        mode_label_index = sorted(collections.Counter(k_means.labels_).items(), key=lambda x: x[1])[-1][0]
        return Point(*k_means.cluster_centers_[mode_label_index])


engine_dict = {
    'feature': FeatureEngine,
    'template': TemplateEngine,
}
