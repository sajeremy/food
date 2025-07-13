from datetime import datetime

from sqlmodel import Session, create_engine, select

from model.groceries import GroceryReceipt, GroceryReceiptSchema, Store, User


def create_user(session: Session, username: str) -> User:
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


def create_store(session: Session, name: str, address: str = None, phone: str = None) -> Store:
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
        user_id=user.id, store_id=store.id if store else None, date_time=date_time, image_content=img_content
    )
    session.add(receipt)
    session.flush()
    return receipt


def add_grocery_receipt_to_db(img_content: bytes, parsed_data: GroceryReceiptSchema, db_url: str):
    """Add a grocery receipt to the database.

    Args:
        img_content (bytes): The image content of the grocery receipt.
        parsed_data (GroceryReceiptSchema): The parsed data from the grocery receipt.
        db_url (str): The database URL.
    """

    engine = create_engine(db_url)
    with Session(engine) as session:
        user = create_user(session=session, username=parsed_data.user.username)

        if parsed_data.store:
            store = create_store(
                session=session,
                name=parsed_data.store.name,
                address=parsed_data.store.address,
                phone=parsed_data.store.phone,
            )

        receipt = create_grocery_receipt(
            session=session, user=user, store=store, date_time=parsed_data.date_time, img_content=img_content
        )

        for purchase in parsed_data.purchases:
            purchase.receipt_id = receipt.id
            session.add(purchase)

        session.commit()
