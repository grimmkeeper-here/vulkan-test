"""
Add: add table rooms
"""

from yoyo import step

__depends__ = {"20240817_01_mYbyf-init-init-database"}

steps = [
    step(
        """
            --- Create table room
            CREATE TABLE room (
                id SERIAL PRIMARY KEY,
                row INT NOT NULL,
                col INT NOT NULL,
                is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            --- Create trigger updated_at
            CREATE TRIGGER update_room_updated_at
            BEFORE UPDATE ON room
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
         """,
        """
            --- Drop trigger update_room_updated_at
            DROP TRIGGER IF EXISTS update_room_updated_at ON room;

            --- Drop table room
            DROP TABLE IF EXISTS room;
         """,
    )
]
