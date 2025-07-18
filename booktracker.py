import sqlite3
import datetime

DATABASE_NAME = 'book_tracker.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                read_date TEXT,
                rating INTEGER,
                notes TEXT
            )
        ''')
        conn.commit()
        print("データベースが初期化されました。")
    except sqlite3.Error as e:
        print(f"データベースの初期化中にエラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()

def add_book():
    print("\n--- 新しい読書記録の追加 ---")
    title = input("タイトル (必須): ").strip()
    if not title:
        print("タイトルは必須です。記録を追加できませんでした。")
        return

    author = input("著者: ").strip()

    while True:
        read_date_str = input("読了日 (YYYY-MM-DD形式、例: 2023-01-15): ").strip()
        if not read_date_str:
            read_date = None # 空の場合はNoneを保存
            break
        try:
            # 日付形式のバリデーション
            datetime.datetime.strptime(read_date_str, '%Y-%m-%d')
            read_date = read_date_str
            break
        except ValueError:
            print("無効な日付形式です。YYYY-MM-DD形式で入力してください。")

    while True:
        rating_str = input("評価 (1〜5の整数、空欄でスキップ): ").strip()
        if not rating_str:
            rating = None # 空の場合はNoneを保存
            break
        try:
            rating = int(rating_str)
            if 1 <= rating <= 5:
                break
            else:
                print("評価は1〜5の整数で入力してください。")
        except ValueError:
            print("無効な入力です。整数を入力してください。")

    notes = input("感想/メモ: ").strip()

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, read_date, rating, notes) VALUES (?, ?, ?, ?, ?)",
            (title, author, read_date, rating, notes)
        )
        conn.commit()
        print(f"'{title}' の記録が追加されました。")
    except sqlite3.Error as e:
        print(f"記録の追加中にエラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()

def view_books():
    print("\n--- 読書記録一覧 ---")
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, read_date, rating, notes FROM books")
        books = cursor.fetchall()

        if not books:
            print("まだ読書記録がありません。")
            return

        # ヘッダーの表示
        print(f"{'ID':<4} | {'タイトル':<30} | {'著者':<20} | {'読了日':<12} | {'評価':<6} | {'感想'}")
        print("-" * 100)

        for book in books:
            book_id, title, author, read_date, rating, notes = book
            # 長いタイトルや感想を省略して表示
            display_title = (title[:27] + '...') if len(title) > 30 else title
            display_author = (author[:17] + '...') if author and len(author) > 20 else (author if author else "N/A")
            display_read_date = read_date if read_date else "N/A"
            display_rating = str(rating) if rating is not None else "N/A"
            display_notes = (notes[:47] + '...') if notes and len(notes) > 50 else (notes if notes else "")

            print(f"{book_id:<4} | {display_title:<30} | {display_author:<20} | {display_read_date:<12} | {display_rating:<6} | {display_notes}")
    except sqlite3.Error as e:
        print(f"記録の表示中にエラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()

def main():
    init_db()

    while True:
        print("\n--- 読書記録アプリ メニュー ---")
        print("1. 新しい記録を追加")
        print("2. 記録を一覧表示")
        print("3. アプリを終了")

        choice = input("選択してください (1-3): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            print("アプリを終了します。")
            break
        else:
            print("無効な選択です。1から3の数字を入力してください。")

if __name__ == '__main__':
    main()
