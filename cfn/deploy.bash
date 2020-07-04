#!/bin/bash

set -xeu

# .ymlなしのファイル名 (=拡張子なし)
template="$1"

base_dir="$(cd $(dirname $0); pwd)"
stack_name="$(echo lambda-cwlogs-s3-$template | tr '_' '-')"
template_filepath="$base_dir/$template.yml"
parameter_filepath="$base_dir/$template.ini"

aws cloudformation deploy \
    --region "ap-northeast-1" \
    --stack-name "$stack_name" \
    --template-file "$template_filepath" \
    --no-fail-on-empty-changeset \
    --capabilities "CAPABILITY_NAMED_IAM" \
    --parameter-overrides $(cat "$parameter_filepath" | tr '\n' ' ')
