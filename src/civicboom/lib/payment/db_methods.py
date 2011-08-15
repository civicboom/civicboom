from civicboom.lib.base import *
from civicboom.model.payment import *

#-------------------------------------------------------------------------------
# Payment actions
#-------------------------------------------------------------------------------
def payment_account_services_normalised(payment_account):
    from civicboom.model.payment import tax_rates
    pacs = [pac.to_dict() for pac in payment_account.services]
    payment_account_types = [pac['service']['payment_account_type'] for pac in pacs]
    if payment_account.type not in payment_account_types:
        this_service = Session.query(Service).filter(Service.payment_account_type == payment_account.type).first()
        if this_service:
            this_service_dict = dict(
                id                  = -1, 
                payment_account_id  = payment_account.id, 
                note                = None, 
                discount            = '0.00', 
                service_id          = this_service.id, 
                service             = this_service.to_dict(),
                #start_date          = payment_account.start_date,
                price               = this_service.get_price(payment_account.currency, payment_account.frequency),
                price_taxed         = (this_service.get_price(payment_account.currency, payment_account.frequency) * Decimal((1 + (tax_rates[payment_account.tax_rate_code] if payment_account.taxable else 0)))).quantize(Decimal('1.00'))
            )
            pacs.append( this_service_dict )
    return pacs

# Create sql where clauses for checking start dates (SQL used as date_part functions are indexed in postgres)
def filter_start_dates(query, frequency, time_now, seven_days):
    if not time_now:
        time_now = now()
    filter = ""
    if frequency == "month":
        # start day:
        filter += "date_part('day', start_date) >= %(day_s)i " % {'day_s':time_now.day}
        # and if end day in same month, else or:
        filter += "and" if seven_days.day > time_now.day else "or"
        # end day:
        filter += " date_part('day', start_date) < %(day_e)i" % {'day_e':seven_days.day}
    elif frequency == "year":
        ## Month 1! & start day:
        filter += "(date_part('month', start_date) = %(month_s)i and date_part('day', start_date) >= %(day_s)i) or " % {'month_s': time_now.month, 'day_s': time_now.day}
        ## Month 2?:
        filter += "(date_part('month', start_date) = %(month_e)i and " % {'month_e': seven_days.month if time_now.month < seven_days.month else time_now.month}
        ##          & end day:
        filter += "date_part('day', start_date) < %(day_e)i)" % {'day_e': seven_days.day}
        
    return query.filter("(%s)" % (filter))

def generate_invoice(account, start_date):
    # Get the service object applicable for this account
    service = Session.query(Service).filter(Service.payment_account_type == account.type).one()
    
    # Create a new Invoice object & set the due date to the service start date
    invoice = Invoice(account)
    invoice.due_date = start_date
    Session.add(invoice)
    Session.commit()
    
    # Check if there is a payment account service set-up for this account (allows discount, etc. to be applied)
    payment_account_service = Session.query(PaymentAccountService).filter(PaymentAccountService.payment_account_id == account.id)\
        .filter(PaymentAccountService.service_id == service.id).first()
    
    # Create billing line for the account's main service type
    line = InvoiceLine(
           invoice,
           payment_account_service  = payment_account_service,
           service                  = service,
           start_date               = start_date
       )
    invoice.lines.append(line)
    
    # Loop through the rest of the services and create billing lines
    # TODO: This needs to take into account service frequency / account frequency, etc.
    for payment_account_service in account.services:
        if payment_account_service.service.payment_account_type != account.type:
            line = InvoiceLine(invoice, payment_account_service.service)
            invoice.lines.append(line)
            #lines.append(line)
    
    # Commit the invoice before changing status or the commit will fail db level security check!
    Session.commit()
    return invoice