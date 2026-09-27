---
name: commit-workflow
description: 실제 변경의 커밋 메시지·단위 또는 push 대상을 준비하거나, 명시된 commit·push 요청을 실행할 때 사용합니다. 메시지 요청을 Git 실행 요청으로 해석하지 않습니다.
---

# Commit Workflow

먼저 요청의 완료 지점을 구별한다. **PREPARE**는 메시지·커밋 단위·push 대상 정보만 제공하며 staging·commit·push·PR을 실행하지 않는다. **EXECUTE**는 사용자가 명시한 commit 또는 push만 현재 권한과 지정 범위에서 수행한다. Commit 요청은 push나 PR을 포함하지 않고, push 요청은 미커밋 변경의 commit을 포함하지 않는다.

적용 지침·커밋 관례와 `git status`를 확인하고 staged, unstaged, untracked를 분리한다. 비밀정보 가능 경로는 내용 출력 전에 선별한다. staged가 있으면 기본 커밋 대상은 staged diff이며, 같은 파일의 unstaged hunk는 제외한다. staged가 없으면 요청과 작업 근거에 맞는 변경만 후보로 삼고 관련 untracked는 경로·유형·내용을 안전하게 확인한다. 무관 변경을 섞지 않는다. 변경이 없으면 메시지를 만들지 않는다.

서로 독립적으로 되돌릴 목적이면 분리를 제안하되 형식 때문에 사용자가 지정한 합리적 범위를 거부하지 않는다. 메시지는 저장소 관례를 우선하고 없으면 간결한 Conventional Commit 제목과 필요한 본문을 작성한다. 검증은 실제 근거가 있는 결과만 쓴다. PREPARE에서는 포함·제외 범위를 분명히 보고한다.

EXECUTE 전에 [실행과 복구](references/execution.md)를 읽는다. 성공은 commit SHA·포함 범위 또는 push remote/ref의 실제 상태로 확인한다. 응답 유실 시 먼저 상태를 조회하고 중복 실행하지 않는다. force push·reset·history rewrite는 일반 요청 범위에 포함되지 않는다.
