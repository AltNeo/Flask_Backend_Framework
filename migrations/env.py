from flask import current_app
from alembic import context
from flask_migrate import Migrate

def run_migrations():
    """Run migrations in 'online' mode."""
    
    # Configure migration context
    config = context.config
    
    # Get database URL from Flask app config
    config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    
    with current_app.app_context():
        # Run the migration
        from app import db
        context.configure(
            connection=db.engine.connect(),
            target_metadata=db.Model.metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
