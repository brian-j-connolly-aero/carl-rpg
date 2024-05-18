import click
from flask.cli import with_appcontext
from flask_app import create_app
from sqlalchemy.inspection import inspect
import models
import services
import inspect as pyinspect

app = create_app()
app.app_context().push()



def prompt_for_updates(current_values):
    updates = {}
    for column, current_value in current_values.items():
        new_value = click.prompt(f"{column} (current: {current_value})", default=current_value)
        updates[column] = new_value
    return updates

def prompt_for_values(model):
    values = {}
    for column in services.get_columns(model):
        value = click.prompt(f"{column}")
        values[column] = value
    return values

def get_model_names():
    """Utility function to get all model names from the models module."""
    return [name for name, obj in pyinspect.getmembers(models) if pyinspect.isclass(obj) and issubclass(obj, models.db.Model)]

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A command-line interface for managing the application.
    """
    if not ctx.invoked_subcommand:
        model_names = get_model_names()
        commands = cli.list_commands(ctx)
        click.echo(cli.help + "\nModels:\n" + "\n".join(model_names) + "\n\nCommands:\n" + "\n".join(commands))
    
    pass

@click.command()
@with_appcontext
def drop_database():
    services.drop_database()

@click.command()
@click.argument('model_name')
@with_appcontext
def list_all(model_name):
    model = getattr(models, model_name, None)
    if not model:
        click.echo(f"Model '{model_name}' not found.")
        return
    entries = services.get_all(model)
    for entry in entries:
        click.echo(f"{entry.ID}: {services.get_by_id(model,entry.ID).Name}")

@click.command()
@click.argument('model_name')
@click.argument('entry_id', type=int)
@with_appcontext
def show(model_name, entry_id):
    model = getattr(models, model_name, None)
    if not model:
        click.echo(f"Model '{model_name}' not found.")
        return
    entry = services.get_by_id(model, entry_id)
    if entry:
        for column, value in services.get_current_values(entry).items():
            click.echo(f"{column}: {value}")
    else:
        click.echo(f"{model_name} entry not found")

@click.command()
@click.argument('model_name')
@with_appcontext
def add(model_name):
    model = getattr(models, model_name, None)
    if not model:
        click.echo(f"Model '{model_name}' not found.")
        return
    data = prompt_for_values(model)
    new_entry = services.create(model, data)
    click.echo(f"{model_name} entry added with ID {new_entry.id}")

@click.command()
@click.argument('model_name')
@click.argument('entry_id', type=int)
@with_appcontext
def update(model_name, entry_id):
    model = getattr(models, model_name, None)
    if not model:
        click.echo(f"Model '{model_name}' not found.")
        return
    entry = services.get_by_id(model, entry_id)
    if entry:
        current_values = services.get_current_values(entry)
        updated_data = prompt_for_updates(current_values)
        services.update(entry, updated_data)
        click.echo(f"{model_name} entry updated")
    else:
        click.echo(f"{model_name} entry not found")

@click.command()
@click.argument('model_name')
@click.argument('entry_id', type=int)
@with_appcontext
def delete(model_name, entry_id):
    model = getattr(models, model_name, None)
    if not model:
        click.echo(f"Model '{model_name}' not found.")
        return
    entry = services.get_by_id(model, entry_id)
    if entry:
        services.delete(entry)
        click.echo(f"{model_name} entry deleted")
    else:
        click.echo(f"{model_name} entry not found")

cli.add_command(drop_database)
cli.add_command(list_all)
cli.add_command(show)
cli.add_command(add)
cli.add_command(update)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
