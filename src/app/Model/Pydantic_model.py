from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator,ConfigDict
from typing import Literal
class DynamicBaseModel(BaseModel):
    model_config=ConfigDict(extra="allow")

class Container(DynamicBaseModel):
    containerNumber: Optional[str] = Field(
        None, description="Container number. Example: 'C123456789'"
    )
    sealNumber: Optional[str] = Field(
        None, description="Seal number. Example: 'SEAL98765'"
    )
    tare: Optional[float] = Field(
        None, description="Container tare weight (kg). Example: 2250.5"
    )
    net: Optional[float] = Field(
        None, description="Net cargo weight (kg). Example: 5000.0"
    )
    grossWeight: Optional[float] = Field(
        None, description="Total weight including container (kg). Example: 7500.0"
    )
    doorType: Optional[str] = Field(
        None, description="Container door type. Example: 'rear', 'fwd'"
    )
    dropMode: Optional[str] = Field(
        None, description="Container drop mode.Example: 'Sideloader', 'Standard Trailer-Drop Trailer'"
    )
    containerSize: Optional[str] = Field(
        None, description="ISO standards for container size. Allowed values: '40REHC', '40RE', '20RE', '400T', '200T', '20FR', '40FR', '20HC', '40HC', '40GP', '20GP'. Example: '40REHC', '20GP'"
    )

    dischargeDate: Optional[datetime] = Field(
        None, description="Date and time of container discharge (ISO 8601). Example: '2024-06-11T10:25:40.834Z'")

    hazardousGood: Optional[bool] = Field(
        None, description="Whether the container contains hazardous materials. Example: True, False"
    )
    

    @field_validator("hazardousGood")
    def validate_hazardous_good(cls, v):
        if v is None:
            return v
        if not isinstance(v, bool):
            raise ValueError("hazardousGood must be a boolean")


    @field_validator("containerSize")
    def validate_container_size(cls, v):
        if v is None:
            return v
        allowed = {
            "40REHC",
            "40RE",
            "20RE",
            "400T",
            "200T",
            "20FR",
            "40FR",
            "20HC",
            "40HC",
            "40GP",
            "20GP"
        }
        if v not in allowed:
            raise ValueError(f"containerSize must be one of {allowed}")
        return v

    

class TypicalTransportJobInformation(DynamicBaseModel):
    jobType: str= Field(..., 
                        description="Classify job type based on context, possible values: IMPORT, EXPORT")
    shipmentType: str= Field(...,
                              description="Shipment type. Example: 'FCL' (Full Container Load), 'LCL' (Less than Container Load)")
    ReferenceNumber: str= Field(...,
                                 description="Unique reference number. Example: 'REF12345'")
    vessel: Optional[str]= Field(None,
                                  description="Vessel name. Example: 'MV Oceanic', 'Ever Given'")
    voyage: Optional[str]= Field(None,
                                  description="Voyage identifier. Example: 'Voyage 123'")
    etd: Optional[datetime]= Field(None,
                                    description="Estimated time of departure (ISO 8601). Example: '2024-06-11T10:25:40.834Z")
    eta: Optional[datetime]= Field(None,
                                    description="Estimated time of arrival (ISO 8601). Example: '2024-06-11T10:25:40.834Z")
    agentClient: Optional[str]= Field(None,
                                       description="Agent or client name. Example: 'Maersk', 'Amazon'")
    consignClient: Optional[str]= Field(None,
                                         description="Consignee receiving the shipment. Example: 'XYZ Imports")
    warehouse: Optional[str]= Field(None,
                                     description="Warehouse handling storage. Example: 'Warehouse 47'")
    accountReceivableClient: Optional[str]= Field(None,
                                                   description="Client responsible for payment. Example: 'Global Finance'")
    jobContainers: Optional[List[Container]] = Field(
        None, description="A list of container information according to the schema"
    )

    
class ImportJobInformation(DynamicBaseModel):
    #Const Jobtype
    jobType: str= Field(..., 
                        description="Classify job type based on context, onnly 1 value: IMPORT")
    shipmentType: str= Field(...,
                              description="Shipment type. Example: 'FCL' (Full Container Load), 'LCL' (Less than Container Load)")

    cusRefNumber: str= Field(...,description="Customs reference number. Example: 'CUS12345'")

    vessel: Optional[str]= Field(None,description="Vessel name. Example: 'MV Oceanic', 'Ever Given'")

    voyage: Optional[str]= Field(None,description="Voyage identifier. Example: 'Voyage 123'")

    unilocoPortOfLoading: Optional[str]= Field(None,description="UN/LOCODE of the port of loading. Example: 'USLAX'.")

    unilocoPortOfDischarge: Optional[str]= Field(None,description="UN/LOCODE of the port of discharge. Example: 'USLAX'.")

    etd: Optional[datetime]= Field(None,description="Estimated time of departure (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    eta: Optional[datetime]= Field(None,description="Estimated time of arrival (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    IMPavailableDate: Optional[datetime]= Field(None,description="Date and time when the import job is available (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    IMPstorageStartDate: Optional[datetime]= Field(None,description="Date and time when the import job is stored (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    firstFreeDay: Optional[datetime]= Field(None,description="First free day for storage (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    IMPstorageLastFreeDate: Optional[datetime]= Field(None,description="Last free day for storage (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    ReeferCutoffDate: Optional[datetime]= Field(None,description="Reefer cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    EmptyReceivalDate: Optional[datetime]= Field(None,description="Empty receival date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    EmptyCutoffDate: Optional[datetime]= Field(None,description="Empty cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    HazardousCutoffDate: Optional[datetime]= Field(None,description="Hazardous cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    HazardousReceivalDate: Optional[datetime]= Field(None,description="Hazardous receival date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    agentClient: Optional[str]= Field(None,
                                       description="Agent or client name. Example: 'Maersk', 'Amazon'")
    consigneeClient: Optional[str]= Field(None,
                                         description="Consignee receiving the shipment. Example: 'XYZ Imports")
    
    warehouse: Optional[str]= Field(None,
                                        description="Warehouse handling storage. Example: 'Warehouse 47'")
    

    accountReceivableClient: Optional[str]= Field(None,
                                                    description="Client responsible for payment. Example: 'Global Finance'")
    
    jobContainers: Optional[List[Container]] = Field(
        None, description="A list of container information according to the schema"
    )
    
    
class ExportJobInformation(DynamicBaseModel):
    #Const Jobtype
    jobType: str= Field(..., 
                        description="Classify job type based on context, onnly 1 value: EXPORT")
    shipmentType: str= Field(...,
                              description="Shipment type. Example: 'FCL' (Full Container Load), 'LCL' (Less than Container Load)")

    cusRefNumber: str= Field(...,description="Customs reference number. Example: 'CUS12345'")

    vessel: Optional[str]= Field(None,description="Vessel name. Example: 'MV Oceanic', 'Ever Given'")

    voyage: Optional[str]= Field(None,description="Voyage identifier. Example: 'Voyage 123'")

    unilocoPortOfLoading: Optional[str]= Field(None,description="UN/LOCODE of the port of loading. Example: 'USLAX'.")

    unilocoPortOfDischarge: Optional[str]= Field(None,description="UN/LOCODE of the port of discharge. Example: 'USLAX'.")

    etd: Optional[datetime]= Field(None,description="Estimated time of departure (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    eta: Optional[datetime]= Field(None,description="Estimated time of arrival (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    EXPreceivalCommencementDate: Optional[datetime]= Field(None,description="Receival commencement date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    ReeferCutoffDate: Optional[datetime]= Field(None,description="Reefer cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    EmptyReceivalDate: Optional[datetime]= Field(None,description="Empty receival date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    EmptyCutoffDate: Optional[datetime]= Field(None,description="Empty cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    HazardousCutoffDate: Optional[datetime]= Field(None,description="Hazardous cutoff date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    HazardousReceivalDate: Optional[datetime]= Field(None,description="Hazardous receival date (ISO 8601). Example: '2024-06-11T10:25:40.834Z")

    agentClient: Optional[str]= Field(None,
                                       description="Agent or client name. Example: 'Maersk', 'Amazon'")
    consignorClient: Optional[str]= Field(None,
                                         description="Consignor receiving the shipment. Example: 'XYZ Imports")
    
    warehouse: Optional[str]= Field(None,
                                        description="Warehouse handling storage. Example: 'Warehouse 47'")
    

    accountReceivableClient: Optional[str]= Field(None,
                                                    description="Client responsible for payment. Example: 'Global Finance'")
    
    jobContainers: Optional[List[Container]] = Field(
        None, description="A list of container information according to the schema"
    )