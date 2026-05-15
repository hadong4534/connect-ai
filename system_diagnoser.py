import os
import sys
from pathlib import Path

# 시스템 진단 로직을 위해 utils 폴더에서 path_validator를 임포트합니다.
try:
    from utils.path_validator import validate_absolute_path, get_required_modules
except ImportError as e:
    print("="*60)
    print("🔴 [CRITICAL ERROR] path_validator.py 모듈을 찾을 수 없습니다.")
    print(f"경로 확인 필요: {e}")
    print("이 스크립트를 실행하기 전에 'connect ai/utils/path_validator.py'가 정상 작동하는지 먼저 검증해야 합니다.")
    sys.exit(1)

# --- [핵심 구성요소 정의] ---
# 프로젝트의 안정적인 운영을 위해 필수적으로 존재하거나, 최소한 설정이 필요하다고 간주되는 모듈과 폴더 목록입니다.
ESSENTIAL_COMPONENTS = {
    "Configuration": {
        "path": "config",
        "description": "애플리케이션 전체에서 사용되는 환경 변수 및 상수 설정을 관리합니다. (예: .env, settings.py)",
        "check_file": ["settings.py", ".env"],
        "required": True
    },
    "API Endpoints": {
        "path": "api",
        "description": "외부 요청을 처리하는 모든 핵심 비즈니스 로직 엔드포인트 모듈이 위치해야 합니다.",
        "check_file": ["user_service.py", "data_fetcher.py"],
        "required": True
    },
    "Utilities": {
        "path": "utils",
        "description": "재사용 가능한 범용 함수(예: 날짜 포맷팅, 유효성 검사)를 담는 모듈 폴더입니다.",
        "check_file": [], # utils 자체는 이미 존재한다고 가정
        "required": True
    },
    "Database Setup": {
        "path": "db",
        "description": "데이터베이스 연결 및 마이그레이션 스크립트가 포함되어야 합니다.",
        "check_file": ["db_setup.py"],
        "required": False # 초기 단계에서는 선택적일 수 있음
    }
}

def run_system_diagnostic():
    """시스템의 전체 구성요소 존재 여부 및 모듈 참조 안정성을 진단합니다."""
    print("="*80)
    print(f"✨ [System Diagnostic Start] 프로젝트 루트: {os.getcwd()}")
    print("==============================================================")

    overall_status = {"passed": True, "warnings": []}

    for component_name, component_data in ESSENTIAL_COMPONENTS.items():
        print(f"\n\n--- [진단 시작] {component_name}: {component_data['description']} ---")
        component_status = {"passed": True, "messages": []}
        component_path = Path(component_data["path"])

        # 1. 폴더 존재 여부 체크 (Path Validation)
        if not component_path.exists():
            msg = f"❌ MISSING: 필수 폴더 '{component_data['path']}'가 존재하지 않습니다."
            print(msg)
            overall_status["warnings"].append(f"[WARNING] {component_name} 폴더 누락: {component_data['description']}")
            component_status["passed"] = False
            component_status["messages"].append("폴더 자체가 없어 아키텍처 수정이 필요합니다.")
            continue # 다음 컴포넌트로 넘어감

        # 2. 필수 파일 존재 여부 체크 (File Validation)
        missing_files = []
        for file_name in component_data["check_file"]:
            full_path = component_path / file_name
            if not full_path.exists():
                missing_files.append(str(full_path))

        if missing_files:
            msg = f"⚠️ [WARNING] {component_name} 폴더 내에 필수 파일이 누락되었습니다."
            print(f"{msg}\n  -> 누락된 파일 목록: {', '.join(missing_files)}")
            overall_status["warnings"].append(f"[WARNING] {component_name} 관련 파일 누락. (예시: {missing_files[0]})")
            component_status["passed"] = False
            component_status["messages"].append("누락된 파일을 추가하여 기능을 보강해야 합니다.")
        else:
             print(f"✅ [PASS] 핵심 폴더 및 파일들이 정상적으로 존재합니다. (경로 안정성 검사 진행...)")


        # 3. 모듈 참조 경로 진단 (PathValidator Integration)
        try:
            # 해당 컴포넌트의 주요 모듈들을 찾아서 절대 경로 유효성을 검증합니다.
            required_modules = get_required_modules(component_path)
            validity_report = validate_absolute_path(required_modules)

            if validity_report['passed']:
                print("✅ [PASS] 모든 모듈의 절대 참조 경로가 유효하며, 안정적으로 연결되어 있습니다.")
            else:
                msg = "❌ [CRITICAL FAIL] 일부 핵심 모듈이 잘못된 상대 경로를 참조하고 있거나 존재하지 않습니다."
                print(f"{msg}\n  -> 상세 진단 결과:\n{validity_report['details']}")
                overall_status["warnings"].append("[ERROR] 절대 경로 참조 오류 발견. 주요 모듈 연결 상태 확인 필요.")
                component_status["passed"] = False
        except Exception as e:
            print(f"❌ [EXCEPTION] Path Validation 중 치명적인 에러 발생: {e}")
            overall_status["warnings"].append(f"[FATAL ERROR] 경로 진단 실패: {e}")
            component_status["passed"] = False

        # 4. 컴포넌트별 종합 보고
        if component_status["passed"]:
            print("🎉 [SUMMARY] <--- " + component_name + " 모듈은 현재 안정적으로 보입니다.")
        else:
            print(f"🚨 [SUMMARY] <--- {component_name} 모듈은 개선이 필요합니다. (경고/오류 확인)")


    # --- 최종 종합 보고서 출력 ---
    print("\n\n" + "="*80)
    if overall_status["passed"] and not overall_status["warnings"]:
        print("✨ [COMPREHENSIVE DIAGNOSIS REPORT] 시스템 안정화 및 통합 준비 상태: ✅ 성공적")
        print("==============================================================")
        print("모든 핵심 구성요소의 존재 여부와 모듈 참조 경로는 현재 정상 범위 내에 있습니다.")
        print("\n💡 [다음 단계 권장 사항]")
        print("- 1. 환경 설정 파일(.env, settings.py)을 점검하여 모든 API 키 및 외부 서비스 토큰이 로드되는지 확인하세요.")
        print("- 2. 단위 테스트(Unit Test)를 실행하여 개별 모듈의 비즈니스 로직 검증에 집중하십시오.")

    else:
        print("🚨 [COMPREHENSIVE DIAGNOSIS REPORT] 시스템 안정화 및 통합 준비 상태: ⚠️ 주의 필요")
        print("==============================================================")
        print("\n[🔍 발견된 주요 문제점 요약]")
        for warning in overall_status["warnings"]:
            print(f" - {warning}")

        print("\n💡 [진단 결과 및 해결책 가이드]")
        print("- 1. **아키텍처 보강:** 누락된 필수 폴더/파일은 해당 기능을 정의하는 코드를 작성하여 추가해야 합니다.")
        print("- 2. **경로 수정:** 절대 경로 참조 오류가 발견된 경우, 스크립트 상단에서 `from ... import ...` 구문을 반드시 수정하여 완전한 절대 경로를 사용하도록 변경해야 합니다.")

    print("="*80)


if __name__ == "__main__":
    run_system_diagnostic()