import psycopg2
import dearpygui.dearpygui as dpg

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="turtlecode"
    )

def insert_user():
    name = dpg.get_value("name_input")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()

    dpg.set_value("name_input", "")
    load_users()

def load_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    dpg.delete_item("user_group", children_only=True)

    for row in rows:
        with dpg.group(parent="user_group", horizontal=True):
            dpg.add_text(f"{row[0]} - {row[1]}")
            dpg.add_spacer(width=40)
            dpg.add_button(
                label="Delete",
                width=150,
                height=50,
                user_data=row[0],
                callback=delete_user
            )

def delete_user(sender, app_data, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    load_users()

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("C:/Windows/Fonts/arial.ttf", 24)

dpg.bind_font(default_font)

with dpg.window(label="Large CRUD App", width=1100, height=800):

    dpg.add_spacer(height=40)

    dpg.add_text("User Name")
    dpg.add_spacer(height=10)

    dpg.add_input_text(
        tag="name_input",
        width=600
    )

    dpg.add_spacer(height=20)

    dpg.add_button(
        label="Add User",
        width=300,
        height=70,
        callback=insert_user
    )

    dpg.add_separator()
    dpg.add_spacer(height=20)

    dpg.add_text("User List:")
    dpg.add_spacer(height=20)

    dpg.add_group(tag="user_group")

dpg.create_viewport(title="Large CRUD", width=1200, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()

load_users()

dpg.start_dearpygui()
dpg.destroy_context()