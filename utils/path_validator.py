import os
from pathlib import Path

def check_absolute_path(target_file: str, reference_dir: str) -> str:
    """주어진 파일 이름과 기준 디렉토리를 조합하여 절대 경로를 반환하고 검증한다."""
    try:
        # 1. os.path.join으로 운영체제에 맞는 경로를 결합
        full_path = os.path.join(reference_dir, target_file)
        
        # 2. os.path.abspath로 절대 경로로 변환 (가장 중요!)
        absolute_path = os.path.abspath(full_path)
        
        print(f"✅ 검증 성공: {target_file} -> [절대] {absolute_path}")
        return absolute_path
    except Exception as e:
        # 에러 발생 시, 근본 원인(Root Cause)을 사용자에게 알린다.
        raise IOError(f"❌ 경로 오류 감지: {target_file}. 원인: {e}")

if __name__ == "__main__":
    # 현재 스크립트가 있는 디렉토리를 기준점으로 사용합니다. (상대적 안정성 확보)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    print("=============================================")
    print(f"--- [진단 시작] 현재 실행 컨텍스트: {CURRENT_DIR} ---")

    # 예시: 'data/config.json'을 절대 경로로 변환하고 검증하는 시뮬레이션
    try:
        final_path = check_absolute_path("data/config.json", CURRENT_DIR)
        print(f"테스트 완료. 최종 경로는 {final_path}입니다.")
    except IOError as e:
        print(e)
    print("=============================================")