H/W 2021-06-07 База даних книжок на FastAPI + ormar + postgresql + docker + alembic.

В якості основи використав fastapi-ormar з лекції.

Замінив resume на book, додав роути /books/me/{book_id} з методами GET, PUT i DELETE для книжок юзера.

В GET /books/ можна вибирати книжки за назвою, автором і періодом видання, підставляючи query parameters в url.
В в pydantic сподобався метод .dict(exclude_none=True) - його зручно використовувати при апдейті записів бази. Можливо, в marshmallow теж є щось схоже, але натрапив лише зараз.

Про міграції з sqlite і postgresql. В db.py є клас MainMeta, від якого спадкуються метадані в моделях User i Book. З якихось причин алембік вимагає щоб метадані знаходились безпосередньо в файлах /book/models.py i /user/models.py, тому в цих файлах є дивна стрічка from db import metadata, а в migrations/env.py  - from book.models import metadata. Інакше alembic не підхоплює зміни в моделях. При чому я спробував різні sys.path в migrations/env.py  -це не дало результату.

Postgresql для міграцій потребує asyncpg і psycopg2 (підходить psycopg2-binary). При чому в статтях по цій темі рекомендують задавати url бази як postgresql+psycopg2://{user}:{password}@{host}, але docker видав помилку Keyerror: "postgresql+psycopg2", тому я задав url як postgresql://{user}:{password}@{host}