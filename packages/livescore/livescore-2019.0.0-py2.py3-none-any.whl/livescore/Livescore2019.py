import colorsys
import cv2
from PIL import Image
import pkg_resources

from .LivescoreBase import LivescoreBase
from .details import Alliance2019, OngoingMatchDetails


class Livescore2019(LivescoreBase):
    def __init__(self, **kwargs):
        super(Livescore2019, self).__init__(2019, **kwargs)
        self._match_key = None
        self._match_name = None

    def _getMatchKeyName(self, img, debug_img):
        if self._match_key is None:
            tl = self._transformPoint((155, 6))
            br = self._transformPoint((570, 43))

            raw_match_name = self._parseRawMatchName(self._getImgCropThresh(img, tl, br))
            self._match_key = self._getMatchKey(raw_match_name)
            if self._match_key:
                self._match_name = raw_match_name
            else:
                self._match_name = None

            if self._debug:
                box = self._cornersToBox(tl, br)
                self._drawBox(debug_img, box, (0, 255, 0))

        return self._match_key, self._match_name

    def _getTimeAndMode(self, img, debug_img):
        # Check for match under review
        review_point1 = self._transformPoint((624, 93))
        review_sample1 = img[review_point1[1], review_point1[0], :]
        hsvL = colorsys.rgb_to_hsv(float(review_sample1[2])/255, float(review_sample1[1])/255, float(review_sample1[0])/255)
        review_point2 = self._transformPoint((1279 - 624, 93))
        review_sample2 = img[review_point2[1], review_point2[0], :]
        hsvR = colorsys.rgb_to_hsv(float(review_sample2[2])/255, float(review_sample2[1])/255, float(review_sample2[0])/255)
        if hsvL[0] > 0.116 and hsvL[0] < 0.216 and hsvR[0] > 0.116 and hsvR[0] < 0.216:
            return 0, 'post_match'

        # Find time remaining
        tl = self._transformPoint((640-25, 56))
        br = self._transformPoint((640+25, 82))
        time_remaining = self._parseDigits(self._getImgCropThresh(img, tl, br))

        # Determine mode: 'pre_match', 'auto', 'teleop', or 'post_match'
        mode_point = self._transformPoint((520, 70))
        mode_point2 = self._transformPoint((581, 70))
        mode_sample = img[mode_point[1], mode_point[0], :]
        mode_sample2 = img[mode_point2[1], mode_point2[0], :]

        hsv1 = colorsys.rgb_to_hsv(float(mode_sample[2])/255, float(mode_sample[1])/255, float(mode_sample[0])/255)
        hsv2 = colorsys.rgb_to_hsv(float(mode_sample2[2])/255, float(mode_sample2[1])/255, float(mode_sample2[0])/255)

        if time_remaining is None:
            return None, None

        if time_remaining == 0:
            if hsv1[1] > 0.6 and hsv2[1] > 0.6:  # Both saturated
                mode = 'post_match'
            elif hsv1[1] > 0.6:  # First saturated
                mode = 'auto'  # End of auton
            else:
                mode = 'pre_match'
        elif time_remaining <= 15 and hsv2[1] < 0.6:
            mode = 'auto'
        else:
            mode = 'teleop'

        if self._debug:
            box = self._cornersToBox(tl, br)
            self._drawBox(debug_img, box, (0, 255, 0))
            cv2.circle(debug_img, review_point1, 2, (0, 255, 0), -1)
            cv2.circle(debug_img, review_point2, 2, (0, 255, 0), -1)
            cv2.circle(debug_img, mode_point, 2, (0, 255, 0), -1)
            cv2.circle(debug_img, mode_point2, 2, (0, 255, 0), -1)

        return time_remaining, mode

    def _getFlipped(self, img, debug_img):
        # Sample point to determine red/blue side
        color_point = self._transformPoint((520, 95))
        color_sample = img[color_point[1], color_point[0], :]
        is_flipped = color_sample[0] > color_sample[2]  # More blue than red

        if self._debug:
            cv2.circle(debug_img, color_point, 2, (0, 255, 0), -1)

        return is_flipped

    def _getScores(self, img, debug_img, is_flipped):
        # Left score limits
        left_tl = self._transformPoint((520, 110))
        left_br = self._transformPoint((634, 155))
        # Right score limits
        right_tl = self._transformPoint((644, 110))
        right_br = self._transformPoint((760, 155))

        left_score = self._parseDigits(self._getImgCropThresh(img, left_tl, left_br, white=True))
        right_score = self._parseDigits(self._getImgCropThresh(img, right_tl, right_br, white=True))

        if is_flipped:
            red_score = right_score
            blue_score = left_score
        else:
            red_score = left_score
            blue_score = right_score

        if self._debug:
            left_box = self._cornersToBox(left_tl, left_br)
            right_box = self._cornersToBox(right_tl, right_br)
            self._drawBox(debug_img, left_box, (255, 255, 0) if is_flipped else (255, 0, 255))
            self._drawBox(debug_img, right_box, (255, 0, 255) if is_flipped else (255, 255, 0))

        return red_score, blue_score

    def _getHatchCargoCounts(self, img, debug_img, is_flipped):
        # Left
        left_cargo_ship_hatch_count_tl = self._transformPoint((359, 114))
        left_cargo_ship_hatch_count_br = self._transformPoint((387, 151))
        left_cargo_ship_cargo_count_tl = self._transformPoint((359, 63))
        left_cargo_ship_cargo_count_br = self._transformPoint((387, 100))

        left_rocket1_hatch_count_tl = self._transformPoint((165, 114))
        left_rocket1_hatch_count_br = self._transformPoint((190, 151))
        left_rocket1_cargo_count_tl = self._transformPoint((165, 63))
        left_rocket1_cargo_count_br = self._transformPoint((190, 100))

        left_rocket2_hatch_count_tl = self._transformPoint((61, 114))
        left_rocket2_hatch_count_br = self._transformPoint((86, 151))
        left_rocket2_cargo_count_tl = self._transformPoint((61, 63))
        left_rocket2_cargo_count_br = self._transformPoint((86, 100))

        # Right
        right_cargo_ship_hatch_count_tl = self._transformPoint((1279 - 387, 114))
        right_cargo_ship_hatch_count_br = self._transformPoint((1279 - 359, 151))
        right_cargo_ship_cargo_count_tl = self._transformPoint((1279 - 387, 63))
        right_cargo_ship_cargo_count_br = self._transformPoint((1279 - 359, 100))

        right_rocket1_hatch_count_tl = self._transformPoint((1279 - 190, 114))
        right_rocket1_hatch_count_br = self._transformPoint((1279 - 165, 151))
        right_rocket1_cargo_count_tl = self._transformPoint((1279 - 190, 63))
        right_rocket1_cargo_count_br = self._transformPoint((1279 - 165, 100))

        right_rocket2_hatch_count_tl = self._transformPoint((1279 - 86, 114))
        right_rocket2_hatch_count_br = self._transformPoint((1279 - 61, 151))
        right_rocket2_cargo_count_tl = self._transformPoint((1279 - 86, 63))
        right_rocket2_cargo_count_br = self._transformPoint((1279 - 61, 100))

        # Counts
        left_cargo_ship_hatch_count = self._parseDigits(self._getImgCropThresh(img, left_cargo_ship_hatch_count_tl, left_cargo_ship_hatch_count_br))
        right_cargo_ship_hatch_count = self._parseDigits(self._getImgCropThresh(img, right_cargo_ship_hatch_count_tl, right_cargo_ship_hatch_count_br))
        left_cargo_ship_cargo_count = self._parseDigits(self._getImgCropThresh(img, left_cargo_ship_cargo_count_tl, left_cargo_ship_cargo_count_br))
        right_cargo_ship_cargo_count = self._parseDigits(self._getImgCropThresh(img, right_cargo_ship_cargo_count_tl, right_cargo_ship_cargo_count_br))

        left_rocket1_hatch_count = self._parseDigits(self._getImgCropThresh(img, left_rocket1_hatch_count_tl, left_rocket1_hatch_count_br))
        right_rocket1_hatch_count = self._parseDigits(self._getImgCropThresh(img, right_rocket1_hatch_count_tl, right_rocket1_hatch_count_br))
        left_rocket1_cargo_count = self._parseDigits(self._getImgCropThresh(img, left_rocket1_cargo_count_tl, left_rocket1_cargo_count_br))
        right_rocket1_cargo_count = self._parseDigits(self._getImgCropThresh(img, right_rocket1_cargo_count_tl, right_rocket1_cargo_count_br))

        left_rocket2_hatch_count = self._parseDigits(self._getImgCropThresh(img, left_rocket2_hatch_count_tl, left_rocket2_hatch_count_br))
        right_rocket2_hatch_count = self._parseDigits(self._getImgCropThresh(img, right_rocket2_hatch_count_tl, right_rocket2_hatch_count_br))
        left_rocket2_cargo_count = self._parseDigits(self._getImgCropThresh(img, left_rocket2_cargo_count_tl, left_rocket2_cargo_count_br))
        right_rocket2_cargo_count = self._parseDigits(self._getImgCropThresh(img, right_rocket2_cargo_count_tl, right_rocket2_cargo_count_br))

        if is_flipped:
            red_cargo_ship_hatch_count = right_cargo_ship_hatch_count
            red_cargo_ship_cargo_count = right_cargo_ship_cargo_count
            blue_cargo_ship_hatch_count = left_cargo_ship_hatch_count
            blue_cargo_ship_cargo_count = left_cargo_ship_cargo_count

            red_rocket1_hatch_count = right_rocket1_hatch_count
            red_rocket1_cargo_count = right_rocket1_cargo_count
            blue_rocket1_hatch_count = left_rocket1_hatch_count
            blue_rocket1_cargo_count = left_rocket1_cargo_count

            red_rocket2_hatch_count = right_rocket2_hatch_count
            red_rocket2_cargo_count = right_rocket2_cargo_count
            blue_rocket2_hatch_count = left_rocket2_hatch_count
            blue_rocket2_cargo_count = left_rocket2_cargo_count
        else:
            red_cargo_ship_hatch_count = left_cargo_ship_hatch_count
            red_cargo_ship_cargo_count = left_cargo_ship_cargo_count
            blue_cargo_ship_hatch_count = right_cargo_ship_hatch_count
            blue_cargo_ship_cargo_count = right_cargo_ship_cargo_count

            red_rocket1_hatch_count = left_rocket1_hatch_count
            red_rocket1_cargo_count = left_rocket1_cargo_count
            blue_rocket1_hatch_count = right_rocket1_hatch_count
            blue_rocket1_cargo_count = right_rocket1_cargo_count

            red_rocket2_hatch_count = left_rocket2_hatch_count
            red_rocket2_cargo_count = left_rocket2_cargo_count
            blue_rocket2_hatch_count = right_rocket2_hatch_count
            blue_rocket2_cargo_count = right_rocket2_cargo_count

        if self._debug:
            left_color = (255, 255, 0) if is_flipped else (255, 0, 255)
            right_color = (255, 0, 255) if is_flipped else (255, 255, 0)

            left_cargo_ship_hatch_count_box = self._cornersToBox(left_cargo_ship_hatch_count_tl, left_cargo_ship_hatch_count_br)
            left_cargo_ship_cargo_count_box = self._cornersToBox(left_cargo_ship_cargo_count_tl, left_cargo_ship_cargo_count_br)
            right_cargo_ship_hatch_count_box = self._cornersToBox(right_cargo_ship_hatch_count_tl, right_cargo_ship_hatch_count_br)
            right_cargo_ship_cargo_count_box = self._cornersToBox(right_cargo_ship_cargo_count_tl, right_cargo_ship_cargo_count_br)

            left_rocket1_hatch_count_box = self._cornersToBox(left_rocket1_hatch_count_tl, left_rocket1_hatch_count_br)
            left_rocket1_cargo_count_box = self._cornersToBox(left_rocket1_cargo_count_tl, left_rocket1_cargo_count_br)
            right_rocket1_hatch_count_box = self._cornersToBox(right_rocket1_hatch_count_tl, right_rocket1_hatch_count_br)
            right_rocket1_cargo_count_box = self._cornersToBox(right_rocket1_cargo_count_tl, right_rocket1_cargo_count_br)

            left_rocket2_hatch_count_box = self._cornersToBox(left_rocket2_hatch_count_tl, left_rocket2_hatch_count_br)
            left_rocket2_cargo_count_box = self._cornersToBox(left_rocket2_cargo_count_tl, left_rocket2_cargo_count_br)
            right_rocket2_hatch_count_box = self._cornersToBox(right_rocket2_hatch_count_tl, right_rocket2_hatch_count_br)
            right_rocket2_cargo_count_box = self._cornersToBox(right_rocket2_cargo_count_tl, right_rocket2_cargo_count_br)

            self._drawBox(debug_img, left_cargo_ship_hatch_count_box, left_color)
            self._drawBox(debug_img, left_cargo_ship_cargo_count_box, left_color)
            self._drawBox(debug_img, right_cargo_ship_hatch_count_box, right_color)
            self._drawBox(debug_img, right_cargo_ship_cargo_count_box, right_color)

            self._drawBox(debug_img, left_rocket1_hatch_count_box, left_color)
            self._drawBox(debug_img, left_rocket1_cargo_count_box, left_color)
            self._drawBox(debug_img, right_rocket1_hatch_count_box, right_color)
            self._drawBox(debug_img, right_rocket1_cargo_count_box, right_color)

            self._drawBox(debug_img, left_rocket2_hatch_count_box, left_color)
            self._drawBox(debug_img, left_rocket2_cargo_count_box, left_color)
            self._drawBox(debug_img, right_rocket2_hatch_count_box, right_color)
            self._drawBox(debug_img, right_rocket2_cargo_count_box, right_color)

        return (
            red_cargo_ship_hatch_count, blue_cargo_ship_hatch_count,
            red_cargo_ship_cargo_count, blue_cargo_ship_cargo_count,
            red_rocket1_hatch_count, blue_rocket1_hatch_count,
            red_rocket1_cargo_count, blue_rocket1_cargo_count,
            red_rocket2_hatch_count, blue_rocket2_hatch_count,
            red_rocket2_cargo_count, blue_rocket2_cargo_count,
        )

    def _getRP(self, img, debug_img, is_flipped):
        left_rocketRP_loc = self._transformPoint((557, 99))
        left_habRP_loc = self._transformPoint((597, 99))
        right_rocketRP_loc = self._transformPoint((1279-597, 99))
        right_habRP_loc = self._transformPoint((1279-557, 99))

        left_rocketRP_sample = img[left_rocketRP_loc[1], left_rocketRP_loc[0], :]
        left_habRP_sample = img[left_habRP_loc[1], left_habRP_loc[0], :]
        right_rocketRP_sample = img[right_rocketRP_loc[1], right_rocketRP_loc[0], :]
        right_habRP_sample = img[right_habRP_loc[1], right_habRP_loc[0], :]

        left_rocketRP_hsv = colorsys.rgb_to_hsv(float(left_rocketRP_sample[2])/255, float(left_rocketRP_sample[1])/255, float(left_rocketRP_sample[0])/255)
        left_habRP_hsv = colorsys.rgb_to_hsv(float(left_habRP_sample[2])/255, float(left_habRP_sample[1])/255, float(left_habRP_sample[0])/255)
        right_rocketRP_hsv = colorsys.rgb_to_hsv(float(right_rocketRP_sample[2])/255, float(right_rocketRP_sample[1])/255, float(right_rocketRP_sample[0])/255)
        right_habRP_hsv = colorsys.rgb_to_hsv(float(right_habRP_sample[2])/255, float(right_habRP_sample[1])/255, float(right_habRP_sample[0])/255)

        left_rocketRP = left_rocketRP_hsv[0] > 0.116 and left_rocketRP_hsv[0] < 0.216
        left_habRP = left_habRP_hsv[0] > 0.116 and left_habRP_hsv[0] < 0.216
        right_rocketRP = right_rocketRP_hsv[0] > 0.116 and right_rocketRP_hsv[0] < 0.216
        right_habRP = right_habRP_hsv[0] > 0.116 and right_habRP_hsv[0] < 0.216

        if is_flipped:
            red_rocketRP = right_rocketRP
            red_habRP = right_habRP
            blue_rocketRP = left_rocketRP
            blue_habRP = left_habRP
        else:
            red_rocketRP = left_rocketRP
            red_habRP = left_habRP
            blue_rocketRP = right_rocketRP
            blue_habRP = right_habRP

        if self._debug:
            left_color = (255, 255, 0) if is_flipped else (255, 0, 255)
            right_color = (255, 0, 255) if is_flipped else (255, 255, 0)
            cv2.circle(debug_img, left_rocketRP_loc, 2, left_color, -1)
            cv2.circle(debug_img, left_habRP_loc, 2, left_color, -1)
            cv2.circle(debug_img, right_rocketRP_loc, 2, right_color, -1)
            cv2.circle(debug_img, right_habRP_loc, 2, right_color, -1)

        return (
            red_rocketRP, blue_rocketRP,
            red_habRP, blue_habRP,
        )

    def _getMatchDetails(self, img, force_find_overlay):
        debug_img = None
        if self._debug:
            debug_img = img.copy()

        time_remaining, mode = self._getTimeAndMode(img, debug_img)
        if self._is_new_overlay or force_find_overlay:
            self._match_key = None
        match_key, match_name = self._getMatchKeyName(img, debug_img)
        is_flipped = self._getFlipped(img, debug_img)
        red_score, blue_score = self._getScores(img, debug_img, is_flipped)

        (
            red_cargo_ship_hatch_count, blue_cargo_ship_hatch_count,
            red_cargo_ship_cargo_count, blue_cargo_ship_cargo_count,
            red_rocket1_hatch_count, blue_rocket1_hatch_count,
            red_rocket1_cargo_count, blue_rocket1_cargo_count,
            red_rocket2_hatch_count, blue_rocket2_hatch_count,
            red_rocket2_cargo_count, blue_rocket2_cargo_count,
        ) = self._getHatchCargoCounts(img, debug_img, is_flipped)
        (
            red_rocketRP, blue_rocketRP,
            red_habRP, blue_habRP,
        ) = self._getRP(img, debug_img, is_flipped)

        if self._debug:
            cv2.imshow("ROIs", debug_img)
            cv2.waitKey(1)

        if match_key is not None and red_score is not None \
                and blue_score is not None and time_remaining is not None:
            return OngoingMatchDetails(
                match_key=match_key,
                match_name=match_name,
                mode=mode,
                time=time_remaining,
                red=Alliance2019(
                    score=red_score,
                    cargo_ship_hatch_count=red_cargo_ship_hatch_count,
                    cargo_ship_cargo_count=red_cargo_ship_cargo_count,
                    rocket1_hatch_count=red_rocket1_hatch_count,
                    rocket1_cargo_count=red_rocket1_cargo_count,
                    rocket2_hatch_count=red_rocket2_hatch_count,
                    rocket2_cargo_count=red_rocket2_cargo_count,
                    rocket_rp=red_rocketRP,
                    hab_rp=red_habRP,
                ),
                blue=Alliance2019(
                    score=blue_score,
                    cargo_ship_hatch_count=blue_cargo_ship_hatch_count,
                    cargo_ship_cargo_count=blue_cargo_ship_cargo_count,
                    rocket1_hatch_count=blue_rocket1_hatch_count,
                    rocket1_cargo_count=blue_rocket1_cargo_count,
                    rocket2_hatch_count=blue_rocket2_hatch_count,
                    rocket2_cargo_count=blue_rocket2_cargo_count,
                    rocket_rp=blue_rocketRP,
                    hab_rp=blue_habRP,
                )
            )
        else:
            return None
