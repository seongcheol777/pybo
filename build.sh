#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# 환경변수가 설정된 경우 관리자 계정 자동 생성
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput || true
fi

# 초기 데이터 로드 (DB가 비어있을 때만)
if [ -n "$LOAD_FIXTURES" ]; then
    python manage.py loaddata fixtures/initial_data.json || true
fi
