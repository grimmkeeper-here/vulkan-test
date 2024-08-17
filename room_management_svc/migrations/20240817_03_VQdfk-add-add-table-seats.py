"""
Add: add table seats
"""

from yoyo import step

__depends__ = {"20240817_02_yQ5OV-add-add-table-rooms"}

steps = [
    step(
        """
            --- Create table seat
            CREATE TABLE seat (
                id SERIAL PRIMARY KEY,
                room_id INT NOT NULL REFERENCES room(id) ON DELETE CASCADE,
                pos_x INT NOT NULL,
                pos_y INT NOT NULL,
                is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            --- Create trigger updated_at
            CREATE TRIGGER update_seat_updated_at
            BEFORE UPDATE ON seat
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
         """,
        """
            --- Drop trigger updated_at
            DROP TRIGGER update_seat_updated_at ON seat;

            --- Drop table seat
            DROP TABLE seat;
         """,
    )
]
