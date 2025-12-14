import os
import shutil

import pandas as pd
import requests

from ..config.setting import Setting
from ..search.daum_searcher import DaumImageSearcher
from ..search.google_searcher import GoogleImageSearcher
from ..search.naver_searcher import NaverImageSearcher
from .face_verifier import FaceVerifier


class BatchVerificationProcessor:

    def __init__(self, reference_member_images_dir=None):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(self.current_dir, "../.."))

        s = Setting()
        if reference_member_images_dir is None:
            self.reference_member_images_dir = s.get_reference_photo_path()

        self.searchers = {
            "daum": DaumImageSearcher(s.get_api_key("daum")),
            "naver": NaverImageSearcher(
                s.get_api_key("naver", "client_id"),
                s.get_api_key("naver", "client_secret"),
            ),
            "google": GoogleImageSearcher(
                s.get_api_key("google"), s.get_api_key("google", "cx")
            ),
        }

    def process_members_by_huboid(self, member_group, similarity_threshold=0.62):
        """huboid 기반 기존 데이터에서 일괄 검증 처리"""
        member_csv = os.path.join(self.project_root, "data", f"{member_group}.csv")
        member_df = pd.read_csv(member_csv)

        # 이미지 저장할 임시공간 준비
        tmp_dir = os.path.join(self.current_dir, "tmp")
        if os.path.exists(tmp_dir):
            try:
                shutil.rmtree(tmp_dir)
            except Exception as e:
                print(f"Failed to remove {tmp_dir}: {e}")
        os.makedirs(tmp_dir, exist_ok=True)

        for row in member_df.itertuples():
            # 1. 검증을 위한 이미지 다운로드
            tmp_image = os.path.join(tmp_dir, f"{row.hubo_id}.jpg")
            result = self._download_image(row.photo_url, tmp_image)

            # 2. 이미지 검증
            if result is not None:
                ref_image = os.path.join(
                    self.reference_member_images_dir, f"{row.hubo_id}.JPG"
                )
                face_verifier = FaceVerifier()
                result = face_verifier.verify(ref_image, tmp_image)
                if result.get("verified"):
                    sim = result.get("similarity")
                    try:
                        sim_val = float(sim) if sim is not None else None
                    except (TypeError, ValueError):
                        sim_val = None

                    if sim_val is not None and sim_val < similarity_threshold:
                        print(
                            f"\033[33mVerification result for {row.hubo_id}: {result}\033[0m"
                        )
                    else:
                        print(f"Verification result for {row.hubo_id}: {result}")
                    continue

                print(f"\033[31mVerification FAILED for {row.hubo_id}: {result}\033[0m")

            # 3. 이미지 다운로드 또는 검증 실패시 새로운 이미지 검색
            title_words = self._get_title_words(member_group)
            q = f"{row.name} {title_words}"
            search_results = self._search_images(q)
            print(f"Search results for {row.hubo_id} ({q}): {search_results[0]}")

    def _download_image(self, url, filename):
        try:
            # 기본 요청
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename

            # 403 등 접근 제한 대응: 브라우저 헤더를 모방하여 재시도
            if response.status_code == 403 or response.status_code == 401:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Referer": url,
                    "Connection": "keep-alive",
                }
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    return filename

            print(
                f"\033[31m_download_image failed for {filename} with status code {response.status_code}\033[0m"
            )
        except Exception as e:
            print(f"\033[31m_download_image exception for {filename}: {e}\033[0m")
            return None

    def _get_title_words(self, member_group):
        if member_group == "na22":
            return "국회의원"
        # TODO: 다른 그룹들에 대한 명칭 추가 필요
        elif member_group == "nec8m3":
            return ""  # 시장, 도지사
        elif member_group == "nec8m4":
            return ""  # 시장, 군수, 구청장
        elif member_group == "nec8m5":
            return ""  # 시의원, 도의원
        elif member_group == "nec8m6":
            return ""  # 시의원, 군의원, 구의원
        else:
            return ValueError("Invalid member group")

    def _search_images(self, query):
        image_urls = []

        for potal in ["google", "daum", "naver"]:  # 우선순위: google > daum > naver
            searcher = self.searchers.get(potal)
            if searcher:
                results = searcher.search(query, num_results=3)
                image_urls.extend(results)

        return image_urls


if __name__ == "__main__":
    batch = BatchVerificationProcessor()
    batch.process_members_by_huboid("na22")
