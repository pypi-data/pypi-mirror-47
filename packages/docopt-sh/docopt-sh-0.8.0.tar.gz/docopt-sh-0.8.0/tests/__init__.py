import subprocess
import shlex
from tempfile import NamedTemporaryFile
import os
import io
from contextlib import contextmanager
from docopt_sh.__main__ import main as docopt_sh_main
from docopt_sh.bash import bash_variable_value


def bash_eval_script(script, argv, bash=None):
  argv = ' '.join(map(shlex.quote, argv))
  executable = 'bash' if bash is None else bash[1]
  process = subprocess.run(
    [executable, '-c', 'set - %s; eval "$(cat)"' % argv],
    input=script.encode('utf-8'),
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=2
  )
  return process.returncode, process.stdout.decode('utf-8'), process.stderr.decode('utf-8')


def bash_decl(name, value, bash_version=None):
  if value is None or type(value) in (bool, int, str):
    return 'declare -- {name}={value}'.format(name=name, value=bash_decl_value(value, bash_version))
  if type(value) is list:
    return 'declare -a {name}={value}'.format(name=name, value=bash_decl_value(value, bash_version))
  raise Exception('Unknown value type %s' % type(value))


def bash_decl_value(value, bash_version=None):
  if value is None:
    return '""'
  if type(value) is bool:
    return '"true"' if value else '"false"'
  if type(value) is int:
    return '"{value}"'.format(value=value)
  if type(value) is str:
    return '"{value}"'.format(value=shlex.quote(value).strip("'"))
  if type(value) is list:
    list_tpl = '({value})'
    if bash_version is not None and (int(bash_version[0]) < 4 or int(bash_version[2]) < 4):
      list_tpl = "'({value})'"
    return list_tpl.format(value=' '.join('[{i}]={value}'.format(
      i=i, value=bash_decl_value(v, bash_version)) for i, v in enumerate(value))
    )


def declare_quote(value):
  return value.replace('\\', '\\\\').replace('"', '\\"')


def replace_docopt_params(stream, docopt_params):
  script = stream.read()
  params = '\n'.join([k + '=' + bash_variable_value(v) for k, v in docopt_params.items()])
  script = script.replace('"DOCOPT PARAMS"', params)
  return io.StringIO(script)


@contextmanager
def patched_script(monkeypatch, capsys, name, program_params=[], docopt_params={}, bash=None):
  with monkeypatch.context() as m:
    with open(os.path.join('tests/scripts', name)) as handle:
      script = replace_docopt_params(handle, docopt_params)

    def run(*argv):
      captured = invoke_docopt(m, capsys, stdin=script, program_params=program_params)
      return bash_eval_script(captured.out, argv, bash=bash)
    yield run


@contextmanager
def temp_script(name, docopt_params={}, bash=None):
  with open(os.path.join('tests/scripts', name)) as handle:
    script = replace_docopt_params(handle, docopt_params).read()
  file = NamedTemporaryFile(mode='w', delete=False)
  try:
    file.write(script)
    file.close()

    def run(args):
      executable = 'bash' if bash is None else bash[1]
      process = subprocess.run(
        [executable, file.name] + args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
      )
      return process.returncode, process.stdout.decode('utf-8'), process.stderr.decode('utf-8')
    yield file, run
  finally:
    os.unlink(file.name)


def invoke_docopt(monkeypatch, capsys=None, program_params=[], stdin=None):
  with monkeypatch.context() as m:
    if stdin is not None:
      m.setattr('sys.stdin', stdin)
    m.setattr('sys.argv', ['docopt.sh'] + program_params)
    docopt_sh_main()
    if capsys is not None:
      return capsys.readouterr()
    return None
