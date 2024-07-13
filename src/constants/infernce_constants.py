from enum import Enum


class LogoLabels(str, Enum):
    COCACOLA = 'cocacola'
    PEPSI = 'pepsi'

LABELS_MAPPING = {
    0: LogoLabels.COCACOLA,
    1: LogoLabels.PEPSI
}
