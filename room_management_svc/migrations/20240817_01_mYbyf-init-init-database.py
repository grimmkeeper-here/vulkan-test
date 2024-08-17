"""
Init: init database
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            --- Create function update_updated_at_column
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
         """,
        """
            --- Drop function update_updated_at_column
            DROP FUNCTION update_updated_at_column();
         """,
    )
]
