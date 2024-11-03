from sqlmodel import select

from hygeia import models
from hygeia.botconf import SessionDep


def create_caregiver(
    session: SessionDep, caregiver_id: str, caregiver_name: str
) -> models.Caregiver:
    caregiver = models.Caregiver(id=caregiver_id, name=caregiver_name)
    session.add(caregiver)
    session.commit()
    session.refresh(caregiver)
    return caregiver


def get_caregiver_by_id(session: SessionDep, caregiver_id: str) -> models.Caregiver | None:
    caregiver = session.exec(
        select(models.Caregiver).where(models.Caregiver.id == caregiver_id)
    ).first()
    return caregiver


def get_current_user_patient(
    session: SessionDep, caregiver_id: str, patient_name: str
) -> models.Patient | None:
    patient = session.exec(
        select(models.Patient).where(
            models.Patient.name == patient_name, caregiver_id == caregiver_id
        )
    ).first()
    return patient


def list_current_user_patients(session: SessionDep, caregiver_id: str) -> list[models.Patient]:
    patients = session.exec(
        select(models.Patient).where(models.Patient.caregiver_id == caregiver_id)
    ).all()
    return list(patients)


def delete_caregiver(session: SessionDep, caregiver_id: str) -> None:
    caregiver = session.exec(
        select(models.Caregiver).where(models.Caregiver.id == caregiver_id)
    ).one()
    session.delete(caregiver)
    session.commit()


def create_patient(session: SessionDep, caregiver_id: str, patient_name: str) -> models.Patient:
    patient = models.Patient(name=patient_name, caregiver_id=caregiver_id)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


def get_patient_by_id(session: SessionDep, patient_id: int) -> models.Patient | None:
    patient = session.exec(select(models.Patient).where(models.Patient.id == patient_id)).first()
    return patient


def create_care_report(
    session: SessionDep, caregiver_id: str, patient_id: int, report: str
) -> models.CareReport:
    care_report = models.CareReport(
        caregiver_id=caregiver_id, patient_id=patient_id, report=report
    )
    session.add(care_report)
    session.commit()
    session.refresh(care_report)
    return care_report


def set_default_patient(
    session: SessionDep, caregiver_id: str, patient_id: int
) -> models.Caregiver:
    caregiver = session.exec(
        select(models.Caregiver).where(models.Caregiver.id == caregiver_id)
    ).one()
    caregiver.default_patient_id = patient_id
    session.commit()
    session.refresh(caregiver)
    return caregiver


def list_care_reports(
    session: SessionDep, caregiver_id: str, patient_id: int
) -> list[models.CareReport]:
    care_reports = session.exec(
        select(models.CareReport).where(
            models.CareReport.caregiver_id == caregiver_id,
            models.CareReport.patient_id == patient_id,
        )
    ).all()
    return list(care_reports)
    return list(care_reports)
