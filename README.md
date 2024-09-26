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

-**orthopedic_surgeon_first_name**: {orthopedic_surgeon_first_name}
-**orthopedic_surgeon_surname**: {orthopedic_surgeon_surname}
-**jpg_doctor**: {jpg_doctor}
-**numbers_hr**: {number_hr}
-**adjusted**: {adjusted}
-**number_thr**: {number_thr}
-**number_bmhr**: {number_bmhr}
-**type_of_hr_prosthesis**: {type_of_hr_prosthesis}
-**type_of_thr_prosthesis**: {type_of_thr_prosthesis}
-**operational_technique**: {operational_technique}
-**anesthetic**: {anesthetic}
-**cement_femur_side**: {cement_femur_side}
-**this_joint_capsule_saved_all**: {this_joint_capsule_saved_all}
-**city**: {city}
-**country**: {country}
-**patient-reported_positive_outcomes**: {patient-reported_positive_outcomes}
-**patient-reported_complications**: {patient-reported_complications}
-**cut_muscles_is_fixed_again**: {cut_muscles_is_fixed_again}
-**complete_opera_report_is_given**: {complete_opera_report_is_given}
-**hr_average_size**: {hr_average_size}
-**hr_average_location**: {hr_average_location}
-**assesses_x-ray**: {assesses_x-ray}
-**x-ray_at_discharge**: {x-ray_at_discharge}
-**two-sided_operation**: {two-sided_operation}
-**foreign_patients**: {foreign_patients}
-**address**: {address}
-**street**: {street}
-**local**: {local}
-**postal_code**: {postal_code}
-**phone_normal**: {phone_normal}
-**phone_free_of_charge**: {phone_free_of_charge}
-**fax**: {fax}
-**mobile**: {mobile}
-**email**: {email}
-**homepage**:{homepage}

The dataset was adapted from https://www.resurfacingscan.be/ortopedlistan/drutoml.htm and contains 1032 records. Information from https://www.hipresurfacingsite.com/list-of-doctors.php was also used.  Additionally, ChatGPT provide a summary of reviews for some of the 
most prominent doctors from Healthgrades website.  Some inconsistencies and mistakes in the datasets were resolved by hand.

You can find the data in ['./Find-a-Doctor/data/hip_surgeons.csv'](data/hip_surgeons.csv).