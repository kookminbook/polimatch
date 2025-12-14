import json
from pathlib import Path


class Setting:

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_file = self.base_dir / "config" / "config.json"
        self.load_config()

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            self._config = json.load(f)

        print(f"Configuration loaded from {self.config_file}")

    def get(self, key_path, default=None):
        """
        점(.) 표기법으로 설정 값 가져오기

        Args:
            key_path: "api_keys.daum.api_key" 형식
            default: 기본값

        Returns:
            설정 값

        Example:
            >>> settings.get("api_keys.daum.api_key")
            "your_api_key"
        """
        keys = key_path.split(".")
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    @property
    def api_keys(self):
        """API 키 정보"""
        return self.get("api_keys", {})

    @property
    def paths(self):
        """경로 정보"""
        return self.get("paths", {})

    def get_api_key(self, potal, key="api_key"):
        """
        API 키 가져오기

        Args:
            portal: "daum", "naver", "google"
            key: API 키 종류 (api_key, client_id 등)

        Returns:
            API 키 문자열

        Example:
            >>> from polimatch.config import get_api_key
            >>> naver_id = get_api_key("naver", "client_id")
        """
        return self.get(f"api_keys.{potal}.{key}")

    def get_reference_photo_path(self):
        """참고 사진 경로 가져오기"""
        return self.get("paths.reference_photos")


if __name__ == "__main__":
    setting = Setting()
    print(setting.api_keys)
    print(setting.get_api_key("daum"))
    print(
        setting.get_api_key("naver", "client_id"),
        setting.get_api_key("naver", "client_secret"),
    )
    print(
        setting.get_api_key("google"),
        setting.get_api_key("google", "cx"),
    )

    print(setting.paths)
    print(setting.get_reference_photo_path())
