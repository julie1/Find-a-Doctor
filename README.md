# Find-a-Doctor

This repository is a rag application for finding a doctor.
This project was implemented for 
[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) -
a free course about LLMs and RAG.

## Project overview
We will specialize in the current project to hip surgeons and in particular
those who do hip resurfacing.  Finding names of surgeons, how many HR's they have 
done, whether or not they are recommended by patients, and their locations will be available.


## Dataset

The dataset used in this project contains information about
hip surgeons, including:

- **orthopedic_surgeon_first_name:** orthopedic surgeon's first name
- **orthopedic_surgeon_surname:** orthopedic surgeon's surname
- **jpg_doctor:** on-line photo link
- **numbers_hr:** number of hip resurfacings done by surgeon
- **adjusted:** date that number of hip resurfacings was adjusted
- **number_thr:** number of total hip replacements by surgeon
- **number_bmhr:** number of Birmingham Mid-Head Resections
- **type_of_hr_prosthesis:** type of hip resurfacing prosthesis
- **type_of_thr_prosthesis:** type_of total hip replacement prosthesis
- **operational_technique:** operational technique
- **anesthetic:** anesthetic
- **cement_femur_side:** is prosthesis cemented
- **this_joint_capsule_saved_all:** the joint capsule was completely saved
- **city:** city
- **country:** country
- **patient-reported_positive_outcomes:** patient reported positive outcomes
- **patient-reported_complications:** patient reported complications
- **cut_muscles_is_fixed_again:** muscles cut during surgery repaired
- **complete_opera_report_is_given:** complete surgery report given to patient
- **hr_average_size:** hip resurfacing average size
- **hr_average_location:** posterior, anterior, etc.
- **assesses_x-ray:** assesses x-ray
- **x-ray_at_discharge:** x-ray at discharge
- **two-sided_operation:** both hips done
- **foreign_patient:** foreign patients
- **address:** address
- **street:** street
- **local:** room or suite number
- **postal_code:** postal code
- **phone_normal:** local phone number
- **phone_free_of_charge:** toll free phone number
- **fax:** fax
- **mobile:** mobile phone
- **email:** email address
- **homepage:** homepage url

The dataset was adapted from https://www.resurfacingscan.be/ortopedlistan/drutoml.htm and contains 1032 records. Information from https://www.hipresurfacingsite.com/list-of-doctors.php was also used.  Some inconsistencies and mistakes in the datasets were resolved by hand.

You can find the data in ['./Find-a-Doctor/data/hip_surgeons.csv'](data/hip_surgeons.csv).