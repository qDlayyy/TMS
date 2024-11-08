from src.common import get_all_ids, get_all_ids_where
from src.database import SessionLocal, Events, Tickets
from src.searching import searching_for_places_by_place_id
from src.service import InputCheck, ServiceException


def ticket_booking():
    with SessionLocal() as session:
        events = session.query(Events).all()

    print('\n~ All available events:')
    results = []
    for event in events:
        item = event.__dict__
        place_id = item["place_id"]
        results.append(searching_for_places_by_place_id(session=session, place_id=place_id, item=item))

    for result in results:
        if result['place_name'] != 'The place has been deleted from the database':
            print(
                f'\n\tID: {result["event_id"]}',
                f'\tName: {result["event_name"]}',
                f'\tDate: {result["event_date"]}',
                f'\tDescription: {result["event_description"] if result["event_description"] else "No description for that event"}',
                sep='\n'
            )

    try:
        choice = input('\nChoose the event you want to book tickets to: ')
        choice = InputCheck.inc(target_number=choice)
        if choice not in get_all_ids(Events):
            raise ServiceException('\n### Warning. There is no such event. ###\n')
        else:
            pass

        with SessionLocal() as session:
            all_tickets_list = all_tickets(session=session, event_id=choice)

        if all_tickets_list:
            show_tickets(tickets_list=all_tickets_list)
            chosen_ticket = ticket_choice(tickets_list=all_tickets_list, chosen_event_id=choice)

            if not chosen_ticket:
                print('\n~ Unfortunately this ticket has been already booked.')
            else:
                booking_person = name_determination()
                with SessionLocal() as session:
                    ticket_book(session=session, ticket_id=chosen_ticket, booking_person=booking_person)
                print('\n~ The ticket has been booked.')

        else:
            print('\n~ Unfortunately there are no available tickets for this event.')

    except Exception as e:
        print(e)


def all_tickets(session, event_id):
    tickets = session.query(Tickets).filter_by(event_id=event_id).all()
    if tickets:
        for ticket_id, ticket in enumerate(tickets):
            tickets[ticket_id] = ticket.__dict__
        return tickets
    else:
        return None


def show_tickets(tickets_list):
    for ticket in tickets_list:
        booking_status = ticket["booking"]
        print(
            f'\n\tID: {ticket["id"]}',
            f'\tSeat: {ticket["place"]}',
            f'\tPrice: {ticket["price"]} BYN',
            f'\tBooking Status: {booking_status if booking_status == "Available" else f"Booked by {booking_status}"}',
            sep='\n'
        )


def ticket_choice(tickets_list, chosen_event_id):
    try:
        choice = input('\nChoose id of the ticket you want to book. Be careful not all of them might be available: ')
        choice = InputCheck.inc(target_number=choice)
        if choice not in get_all_ids_where(table_name=Tickets, column_name='event_id', column_value=chosen_event_id):
            raise ServiceException('\n### Warning. There is no such ticket. ###\n')
        else:
            for ticket in tickets_list:
                if ticket['id'] == choice:
                    return choice if ticket['booking'] == 'Available' else None
    except ServiceException as e:
        raise ServiceException('\n### Warning. There is no such ticket. ###\n')
    except Exception as e:
        raise ServiceException('\n### Warning. There are some troubles with booking this ticket. ###\n')


def ticket_book(session, ticket_id, booking_person):
    data = session.query(Tickets).filter(Tickets.id == ticket_id).first()

    setattr(data, 'booking', booking_person)
    session.commit()


def name_determination():
    try:
        booking_person = input('\nEnter the data about the person booking: ')
        booking_person = InputCheck.nes(target_string=booking_person)
    except Exception as e:
        raise ServiceException('\n### Warning. This cannot be used as persons\'s data. ###\n')
    return booking_person