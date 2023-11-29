from models import Authors, Quotes
from mongoengine import connect


def main():
    connect(db="hw08", alias="default",
            host="mongodb+srv://II-777:1234@cluster0.u2illjh.mongodb.net/?retryWrites=true&w=majority")

    while True:
        command = input("Введіть команду: ").strip()

        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            author = Authors.objects(fullname=author_name).first()
            if author:
                quotes = Quotes.objects(author=author)
                for q in quotes:
                    print(q.quote)
            else:
                print(f"Автор {author_name} не знайдений.")

        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = Quotes.objects(tags=tag)
            for q in quotes:
                print(q.quote)

        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(',')
            quotes = Quotes.objects(tags__in=tags)
            for q in quotes:
                print(q.quote)

        elif command == "exit":
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
