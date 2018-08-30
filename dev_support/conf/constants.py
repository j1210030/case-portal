GENDER_CHOICES =(
        ('M','Male'),
        ('F','Female'),
        ('ND','Not disclosed'),
    )

LANGUAGE_CHOICES =(
        ('en','English'),
        ('jp','Japanese'),
        ('zh','Chinese'),
        ('ko','Korean'),
    )

GEO_LOCATION_CHOICES =(
        ('jp','Japan'),
        ('zh','China'),
        ('ko','Korea'),
    )

PARTNER_STATUS_CHOICES =(
        (True,'Active'),
        (False,'Inactive'),
    )

GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female'),
    )

CASE_REVIEW_STATUS_CHOICES=(
        ('Open','Open'),
        ('NG','NG'),
        ('OK','OK'),
        ('Cancelled','Cancelled'),
    )

CASE_STATUS_CHOICES =(
        ('assigned','Assigned'),
        ('needinfo','Need Info'),
        ('inconsult','In Consult'),
        ('blocked','Blocked'),
        ('solution_offered','Solution offered'),
        ('routed','Routed'),
        ('review_requested','DA Review requested'),
        ('forwarded','Forwarded to MNL/MTV'),
        ('duplicate','Duplicate'),
    )

CASE_DIFFICULTY_CHOICES =(
        ('easy','Easy'),
        ('moderate','Moderate'),
        ('complex','Complex'),
        ('very_complex','Very Complex ')
    )

PRODUCT_CHOICES =(
        ('android','Android'),
        ('firebase','Firebase'),
        ('chrome','Chrome'),
        ('google-apps','Google Apps')
    )

SUB_PRODUCT_CHOICES =(
        ('ios','iOS'),
        ('android','Android'),
        ('web','Web'),
        ('combined','Combined'),
        ('other','Other'),
    )