from datetime import datetime

from sqlmodel import Session, create_engine, select

from orm.data_models import (
    GroceryCategory,
    GroceryReceipt,
    GroceryReceiptSchema,
    Item,
    Purchase,
    Store,
    Transaction,
    User,
)


def get_or_create_user(session: Session, username: str) -> User:
    """Create a new user or retrieve an existing one.

    Args:
        session (Session): The database session.
        username (str): The username of the user.

    Returns:
        User: The created or retrieved user.
    """

    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        user = User(username=username)
        session.add(user)
        session.flush()
    return user


def get_or_create_store(session: Session, name: str = "unknown", address: str = None, phone: str = None) -> Store:
    """Create a new store or retrieve an existing one.

    Args:
        session (Session): The database session.
        name (str): The name of the store.
        address (str, optional): The address of the store. Defaults to None.
        phone (str, optional): The phone number of the store. Defaults to None.

    Returns:
        Store: The created or retrieved store.
    """
    store = session.exec(select(Store).where(Store.name == name)).first()

    if not store:
        store = Store(name=name, address=address, phone=phone)
        session.add(store)
        session.flush()
    return store


def create_grocery_receipt(
    session: Session,
    user: User,
    store: Store,
    date_time: datetime,
    img_content: bytes,
) -> GroceryReceipt:
    """Create a grocery receipt in the database.

    Args:
        session (Session): The database session.
        user (User): The user associated with the receipt.
        store (Store): The store where the purchase was made.
        date_time (datetime): The date and time of the purchase.
        img_content (bytes): The image content of the receipt.

    Returns:
        GroceryReceipt: The created grocery receipt.
    """
    receipt = GroceryReceipt.from_image_and_data(
        user_id=user.id, store_id=store.id, date_time=date_time, image_content=img_content
    )
    session.add(receipt)
    session.flush()
    return receipt


def get_or_create_item(
    session: Session, store_id: int, name: str, category: GroceryCategory, brand: str | None = None
) -> Item:
    """Create a new item or retrieve an existing one.

    Args:
        session (Session): The database session.
        store_id (int): The ID of the store where the item is sold.
        name (str): The name of the item.
        category (GroceryCategory): The category of the item.
        brand (str | None, optional): The brand of the item. Defaults to None.

    Returns:
        Item: The created or retrieved item.
    """
    item = session.exec(select(Item).where(Item.name == name, Item.store_id == store_id)).first()

    if not item:
        item = Item(name=name, category=category, brand=brand, store_id=store_id)
        session.add(item)
        session.flush()
    return item


def create_transaction_from_purchase(
    session: Session,
    purchase: Purchase,
    receipt_id: int,
    store_id: int,
) -> Transaction:
    """Create a new transaction from a purchase.

    Args:
        session (Session): The database session.
        purchase (Purchase): The purchase to create a transaction for.
        receipt_id (int): The ID of the grocery receipt.
        store_id (int): The ID of the store.

    Returns:
        Transaction: The created transaction.
    """

    item = get_or_create_item(
        session=session,
        store_id=store_id,
        name=purchase.name,
        category=purchase.category,
        brand=purchase.brand,
    )
    transaction = Transaction(
        receipt_id=receipt_id,
        item_id=item.id,
        quantity=purchase.quantity,
        unit_price=purchase.unit_price,
        unit_type=purchase.unit_type,
    )
    session.add(transaction)
    session.flush()
    return transaction


def is_receipt_in_db(img_content: bytes, db_url: str) -> bool:
    """Check if a grocery receipt already exists in the database.

    Args:
        img_content (bytes): The image content of the grocery receipt.
        db_url (str): The database URL.

    Returns:
        bool: True if the receipt exists, False otherwise.
    """
    img_hash = GroceryReceipt.generate_image_hash(img_content)
    engine = create_engine(db_url)

    with Session(engine) as session:
        existing_receipt = session.exec(select(GroceryReceipt).where(GroceryReceipt.image_hash == img_hash)).first()
        return existing_receipt is not None


def add_grocery_receipt_to_db(img_content: bytes, parsed_data: GroceryReceiptSchema, db_url: str):
    """Add a grocery receipt to the database.

    Args:
        img_content (bytes): The image content of the grocery receipt.
        parsed_data (GroceryReceiptSchema): The parsed data from the grocery receipt.
        db_url (str): The database URL.
    """
    engine = create_engine(db_url)

    with Session(engine) as session:
        user = get_or_create_user(session=session, username=parsed_data.user.username)

        if parsed_data.store:
            store = get_or_create_store(
                session=session,
                name=parsed_data.store.name,
                address=parsed_data.store.address,
                phone=parsed_data.store.phone,
            )

        receipt = create_grocery_receipt(
            session=session, user=user, store=store, date_time=parsed_data.date_time, img_content=img_content
        )

        for purchase in parsed_data.purchases:
            create_transaction_from_purchase(
                session=session,
                purchase=purchase,
                receipt_id=receipt.id,
                store_id=store.id,
            )

        session.commit()
