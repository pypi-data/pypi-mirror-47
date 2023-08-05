import os

from dvc.exceptions import MoveNotDataSourceError
from dvc.repo.scm_context import scm_context


def _expand_target_path(from_path, to_path):
    if os.path.isdir(to_path):
        return os.path.join(to_path, os.path.basename(from_path))
    return to_path


@scm_context
def move(self, from_path, to_path):
    """
    Renames an output file and modifies the stage associated
    to reflect the change on the pipeline.

    If the output has the same name as its stage, it would
    also rename the corresponding stage file.

    E.g.
          Having: (hello, hello.dvc)

          $ dvc move hello greetings

          Result: (greeting, greeting.dvc)

    It only works with outputs generated by `add` or `import`,
    also known as data sources.
    """
    import dvc.output as Output
    from dvc.stage import Stage

    from_out = Output.loads_from(Stage(self), [from_path])[0]

    to_path = _expand_target_path(from_path, to_path)

    outs = self.find_outs_by_path(from_out.path)
    assert len(outs) == 1
    out = outs[0]
    stage = out.stage

    if not stage.is_data_source:
        raise MoveNotDataSourceError(stage.relpath)

    stage_name = os.path.splitext(os.path.basename(stage.path))[0]
    from_name = os.path.basename(from_out.path)
    if stage_name == from_name:
        os.unlink(stage.path)

        stage.path = os.path.join(
            os.path.dirname(to_path),
            os.path.basename(to_path) + Stage.STAGE_FILE_SUFFIX,
        )

        stage.wdir = os.path.abspath(
            os.path.join(os.curdir, os.path.dirname(to_path))
        )

    to_out = Output.loads_from(
        stage, [os.path.basename(to_path)], out.use_cache, out.metric
    )[0]

    with self.state:
        out.move(to_out)

    stage.dump()
