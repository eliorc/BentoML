#!/usr/bin/env bash

# Prerequisite:
# This scripts assumes BentoML and all its test dependencies are already installed:
#  
#  pip install -e .
#  pip install requirements/tests-requirements.txt


fname=$(basename "$0")
dname=$(dirname "$0")

source "$dname/helpers.sh"

set_on_failed_callback "ERR=1"

GIT_ROOT=$(git rev-parse --show-toplevel)

ERR=0

declare -a PYTESTARGS
CONFIG_FILE="$dname/config.yml"
REQ_FILE="/tmp/additional-requirements.txt"
SKIP_DEPS=0

cd "$GIT_ROOT" || exit

run_yq() {
  need_cmd yq
  yq "$@";
}

getval(){
  run_yq eval "$@" "$CONFIG_FILE";
}

run_python(){
  python -m "$@"
}

validate_yaml() {
  # validate YAML file
  if ! [ -f "$CONFIG_FILE" ]; then
    FAIL "$CONFIG_FILE does not exists"
    exit 1
  fi

  if ! (run_yq e --exit-status 'tag == "!!map" or tag== "!!seq"' "$CONFIG_FILE"> /dev/null); then
    FAIL "Invalid YAML file"
    exit 1
  fi
}


usage() {
  need_cmd cat

  cat <<HEREDOC
Running unit/integration tests with pytest and generate coverage reports. Make sure that given testcases is defined under $CONFIG_FILE.

Usage:
  $dname/$fname [-h|--help] [-v|--verbose] [-s|--skip_deps] <target> <pytest_additional_arguments>

Flags:
  -h, --help            show this message
  -v, --verbose         set verbose scripts
  -s, --skip_deps       skip install dependencies


If pytest_additional_arguments is given, this will be appended to given tests run.

Example:
  $ $dname/$fname pytorch --gpus
HEREDOC
  exit 2
}


parse_args() {
  if [ "${#@}" -eq 0 ]; then
    FAIL "$0 doesn't run without any arguments";
    exit 1;
  fi

  for arg in "$@"; do
    case "$arg" in
      -h | --help)
        usage;;
      -v | --verbose)
        set -x;
        shift;;
      -s | --skip_deps)
        SKIP_DEPS=1;
        shift;;
      *)
        ;;
    esac
  done
  PYTESTARGS=( "${*:2}" )
  shift $(( OPTIND - 1 ))
}


parse_config() {
  target=$@
  test_dir=
  is_dir=
  override_name_or_path=
  external_scripts=
  type_tests=

  test_dir=$(getval ".$target.root_test_dir")
  is_dir=$(getval ".$target.is_dir")
  override_name_or_path=$(getval ".$target.override_name_or_path")
  external_scripts=$(getval ".$target.external_scripts")
  type_tests=$(getval ".$target.type_tests")

  # processing file name
  if [[ "$override_name_or_path" != "" ]]; then
    fname="$override_name_or_path"
  elif [[ "$is_dir" == "false" ]]; then
    fname="test_""$target""_impl.py"
  elif [[ "$is_dir" == "true" ]]; then
    fname=""
  else
    fname="$target"
  fi

  # processing dependencies
  run_yq eval '.'"$target"'.dependencies[]' "$CONFIG_FILE" >"$REQ_FILE" || exit
}

install_yq() {
  target_dir="$HOME/.local/bin"

  mkdir -p "$target_dir"
  export PATH=$target_dir:$PATH

  YQ_VERSION=4.14.2
  echo "Trying to install yq..."
  __shell=$(uname | tr '[:upper:]' '[:lower:]')
  YQ_BINARY=yq_"$__shell"_amd64
  curl -fsSLO https://github.com/mikefarah/yq/releases/download/v"$YQ_VERSION"/"$YQ_BINARY".tar.gz
  echo "tar $YQ_BINARY.tar.gz and move to /usr/bin/yq..."
  tar -zvxf "$YQ_BINARY.tar.gz" "./$YQ_BINARY" && mv "./$YQ_BINARY" "$target_dir"/yq
  rm -f ./"$YQ_BINARY".tar.gz
}


main() {
  parse_args "$@"

  need_cmd make
  need_cmd curl
  need_cmd tr
  (need_cmd yq && echo "Using yq via $(which yq)...";) || install_yq

  run_python pip install -U pip setuptools


  for args in "$@"; do
    if [[ "$args" != "-"* ]]; then
      argv="$args"
      break;
    else
      shift;
    fi
  done

  #  validate_yaml
  parse_config "$argv"

  OPTS=(--cov=bentoml --cov-config="$GIT_ROOT"/setup.cfg --cov-report=xml:"$target.xml")

  if [ -n "${PYTESTARGS[*]}" ]; then
    # shellcheck disable=SC2206
    OPTS=( ${OPTS[@]} ${PYTESTARGS[@]} )
  fi

  if [ "$SKIP_DEPS" -eq 0 ]; then
    # setup tests environment
    if [ -f "$REQ_FILE" ]; then
      run_python pip install -r "$REQ_FILE" || exit 1
    fi
  fi

  if [ -n "$external_scripts" ]; then
    eval "$external_scripts" || exit 1
  fi

  if [ "$type_tests" == 'e2e' ]; then
    cd "$GIT_ROOT"/"$test_dir"/"$fname" || exit 1
    path="."
  else
    path="$GIT_ROOT"/"$test_dir"/"$fname"
  fi

  if ! (run_python pytest "$path" "${OPTS[@]}"); then
    ERR=1
  fi

  # Return non-zero if pytest failed
  if ! test $ERR = 0; then
    FAIL "$args $type_tests tests failed!"
    exit 1
  fi

  PASS "$args $type_tests tests passed!"
}

main "$@" || exit 1

# vim: set ft=sh ts=2 sw=2 tw=0 et :