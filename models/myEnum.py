import enum


class Sex(enum.Enum):
    Men = 1,
    Women = 2,
    Other = 3
    
    
class RoomStatus(enum.Enum):
    AVAILABLE = "Available"
    PENDING = "Pending"
    BOOKED = "Booked"


class BookingStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    CHECKED_IN = "Checked-in"
    CHECKED_OUT = "Checked-out"
    NO_SHOW = "No-show"
    OVERDUE = "Overdue"
    ON_HOLD = "On-hold"
    ERROR = "Error"
    
