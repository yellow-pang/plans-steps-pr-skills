# Commit·Push 실행과 복구

사용자의 현재 요청과 이전에 명확히 지정된 범위를 재사용한다. 실행 직전 status·index·대상 branch/remote/ref를 다시 확인한다. 기존 사용자 변경과 제외 hunk를 보존한다. 무관 staged가 섞였고 안전하게 분리할 수 없다면 index를 임의로 지우지 말고 구체 범위를 확인한다.

Commit: staged가 요청 범위와 맞으면 그것만 commit한다. staged가 없으면 요청에 관련된 변경만 선택 staging한다. 같은 파일의 제외할 unstaged 변경을 `git add <file>`로 끌어들이지 않는다. 이미 확정된 실행 요청에 메시지 사전 승인을 반복 요구하지 않는다. hook이 내용을 바꾸면 포함 범위와 관련 검증을 다시 확인한다. Commit 요청만으로 모든 테스트를 강제하지 않으며, 관련 내용·환경과 실행 근거가 유효하면 재사용한다. 미실행·실패를 성공이라고 쓰지 않는다.

여러 줄 메시지는 UTF-8 임시 파일에 실제 개행으로 기록하고 `git commit --file <path>`로 전달한다. 셸 문자열에 본문을 삽입해 변수·명령이 재해석되거나 문자 `\n`이 그대로 저장되게 하지 않는다. commit 후 `git show -s --format=%B HEAD` 등으로 저장된 한국어 제목·본문·개행을 확인하고, 실제 포함 diff와 남은 변경도 대조한다. 메시지 이상을 발견해도 임의 amend로 이력을 수정하지 말고 상태와 필요한 조치를 보고한다.

Push: 기존 commit의 대상 remote/ref와 공개할 commit 범위를 확인한다. 모호하거나 금지된 대상이면 해당 실행만 보류한다. 일반 push 범위 밖의 force·history rewrite·무관 branch 공개를 추정하지 않는다.

Timeout·응답 유실·부분 실패 시 mutation을 다시 보내기 전에 HEAD, index, remote ref를 조회한다. 완료한 동작과 실패 또는 미확인 동작, 보존한 변경, 다음 조치를 구분해 보고한다. 결과가 불확실하면 성공을 주장하거나 중복 commit을 만들지 않는다.
