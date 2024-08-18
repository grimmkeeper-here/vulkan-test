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
                room_id INT REFERENCES room(id),
                pos_x INT NOT NULL,
                pos_y INT NOT NULL,
                is_deleted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE UNIQUE INDEX idx_room_pos ON seat (room_id, pos_x, pos_y);

            --- Create trigger updated_at
            CREATE TRIGGER update_seat_updated_at
            BEFORE UPDATE ON seat
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
         """,
        """
            --- Drop trigger updated_at
            DROP TRIGGER update_seat_updated_at ON seat;

            -- Drop the index
            DROP INDEX IF EXISTS idx_room_pos;

            --- Drop table seat
            DROP TABLE IF EXISTS seat;
         """,
    )
]
