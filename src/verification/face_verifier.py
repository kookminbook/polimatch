from deepface import DeepFace


class FaceVerifier:
    def __init__(self, detect_backend="mtcnn"):
        self.detect_backend = detect_backend

    def verify(self, image1_path, image2_path):
        try:
            result = DeepFace.verify(
                image1_path, image2_path, detector_backend=self.detect_backend
            )
            similarity = self._calculate_similarity(
                result["distance"], result["threshold"]
            )
            confidence = self._assess_confidence(
                result["distance"], result["threshold"]
            )

            return {
                "verified": result["verified"],
                "distance": result["distance"],
                "threshold": result["threshold"],
                "similarity": similarity,
                "confidence": confidence,
            }

        except Exception as e:
            print(f"Error during face verification: {e}")
            return {"verified": False, "error": str(e)}

    def _calculate_similarity(self, distance, threshold):
        """거리값을 유사도 점수로 변환 (0~1)"""
        # 거리가 0이면 1.0, threshold보다 크면 0에 가까움
        if distance == 0:
            return 1.0
        similarity = max(0, 1 - (distance / (threshold * 2)))
        return round(similarity, 4)

    def _assess_confidence(self, distance, threshold):
        """신뢰도 등급 평가"""
        gap = abs(distance - threshold)
        if gap > threshold * 0.3:
            return "high"
        elif gap > threshold * 0.1:
            return "medium"
        else:
            return "low"


if __name__ == "__main__":
    verifier = FaceVerifier()
    result = verifier.verify("image1.jpg", "image2.jpg")
    print(f"Verification result: {result}")
