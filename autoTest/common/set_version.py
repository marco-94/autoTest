import re


class SetVersion:
    @staticmethod
    def model_version(version):
        """
        编辑时版本号的变化
        """
        rule = r"\d+"
        version_1 = int(re.findall(rule, version)[0])
        version_2 = int(re.findall(rule, version)[1])
        version_3 = int(re.findall(rule, version)[2])
        version_3 += 1
        if version_3 == 10:
            version_3 = 0
            version_2 += 1
            if version_2 == 10:
                version_2 = 0
                version_1 += 1
        version = "V" + str(version_1) + "." + str(version_2) + "." + str(version_3)
        return version
