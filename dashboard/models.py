import uuid

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from cities_light.models import Country
from django.db import models

CURRENCIES = (
    ("", "Select Curency"),
    ("$", "$"),
)

CATEGORY_TYPES = (
    ("", "Select Category Type"),
    ("ASS", "Asset"),
    ("ACP", "Access Point"),
    ("CHS", "Chassis"),
    ("CMP", "Computer"),
    ("SWT", "Switch"),
    ("RTR", "Router"),
    ("FRW", "Firewall"),
    ("PRT", "Printer"),
    ("SCN", "Scanner"),
    ("PRJ", "Projector"),
    ("PHN", "Phone"),
    ("TBL", "Tablet"),
    ("MPH", "Mobile Phone"),
    ("VCF", "Video Conference"),
    ("VGW", "VoIP Gateway"),
    ("VPH", "VoIP Phone"),
    ("Monitor", "Monitor"),
    ("KVM", "KVM (Keyboard, Video, Mouse switch)"),
    ("BLC", "Load Balancer"),
    ("SAN", "SAN (Storage Area Network)"),
    ("NAS", "NAS (Network Attached Storage)"),
    ("TLB", "Tape Library"),
    ("UPS", "UPS"),
    ("GNR", "General Purpose"),
    ("OCP", "Other Computer Device"),
    ("ONP", "Other Network Device"),
    ("OSD", "Other Security Device"),
    ("OGD", "Other Storage Device"),
    ("OTD", "Other Telecom Device"),
    ("OTH", "Other Device"),
)

MEMORY_TYPES = (
    ("", "Select Type"),
    ("TB", "TB"),
    ("GB", "GB"),
    ("MB", "MB"),
)


class Company(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

class Location(models.Model):
    name = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    location_currency = models.CharField(null=True, max_length=255, choices=CURRENCIES, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)

    def __str__(self):
        return self.name

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

class Supplier(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    fax_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="suppliers", blank=True)

    def __str__(self):
        return self.name

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

class Software(models.Model):
    name = models.CharField(max_length=255, null=True)
    serial = models.CharField(max_length=255, null=True, blank=True)
    licensed_to_name = models.CharField(max_length=255, null=True, blank=True)
    licensed_to_email = models.EmailField(blank=True, null=True)
    seats = models.IntegerField(null=True, blank=True)
    reassignable = models.BooleanField(default=False, blank=True)
    maintained = models.BooleanField(default=False, blank=True)
    supplier = models.ForeignKey("Supplier", null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_os = models.BooleanField(default=False, blank=True)
    assigned_to = models.ForeignKey("DashUser", null=True, blank=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

auditlog.register(Software, exclude_fields=[])


class Hardware(models.Model):
    manufacturer = models.ForeignKey("Manufacturer", null=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY_TYPES)
    model = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="suppliers", blank=True)

    def __str__(self):
        return self.model

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)


class Asset(models.Model):
    STATUS = (
        ("", "Select Status"),
        ("Ready to Deploy", "Ready to Deploy"),
        ("Unassign", "Unassign"),
    )
    PLATFORMS = (
        ("", "Select Platform"),
        ("Physical", "Physical"),
        ("Virtual", "Virtual"),
        ("Azure", "Azure"),
        ("Amazon Web Services", "Amazon Web Services"),
    )

    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Asset Name")
    asset_tag = models.CharField(max_length=12, editable=False, default="UNKNOWN", verbose_name="Asset Tag")
    memory_size = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True,
                                      verbose_name="Memory Size")
    memory_type = models.CharField(max_length=255, null=True, choices=MEMORY_TYPES, blank=True,
                                   verbose_name="Memory Type")
    cpu_speed = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True, verbose_name="Cpu Speed")
    cpu_count = models.IntegerField(null=True, blank=True, verbose_name="CPU Count")
    disk_size = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True, verbose_name="Disk Size")
    disk_type = models.CharField(max_length=255, null=True, choices=MEMORY_TYPES, blank=True, verbose_name="Disk Type")
    ip_address = models.CharField(null=True, blank=True, max_length=255, verbose_name="IP Address")
    role = models.CharField(max_length=255, null=True, blank=True, verbose_name="Role")
    os = models.ForeignKey("Software", null=True, blank=True, related_name="os", verbose_name="Operating System")
    platform = models.CharField(max_length=255, null=True, choices=PLATFORMS, blank=True, verbose_name="Platform")
    serial = models.CharField(max_length=255, null=True, blank=True, verbose_name="Serial")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="Purchase Date")
    order_number = models.IntegerField(null=True, blank=True, verbose_name="Order Number")
    purchase_cost = models.DecimalField(max_digits=64, decimal_places=2, null=True, blank=True,
                                        verbose_name="Purchase Cost")
    warranty = models.IntegerField(null=True, blank=True, verbose_name="Warranty")
    notes = models.TextField(null=True, blank=True, verbose_name="Notes")
    location = models.ForeignKey("Location", null=True, blank=True, verbose_name="Location")
    supplier = models.ForeignKey("Supplier", null=True, blank=True, verbose_name="Supplier")
    application = models.ManyToManyField("Software", blank=True, related_name='software',
                                         verbose_name="Assigned Software")
    model = models.ForeignKey("Hardware", null=True, verbose_name="Hardware Model")
    status = models.CharField(max_length=255, null=True, choices=STATUS, verbose_name="Status")
    company = models.ForeignKey("Company", null=True, blank=True, verbose_name="Company")
    assigned_to = models.ForeignKey("DashUser", null=True, blank=True, verbose_name="User Assigned")
    history = AuditlogHistoryField()

    def __str__(self):
        return self.asset_tag

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)


auditlog.register(Asset, exclude_fields=['asset_tag', 'id', ])


class DashUser(models.Model):
    fullname = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return self.fullname

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

auditlog.register(DashUser, exclude_fields=[])


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)