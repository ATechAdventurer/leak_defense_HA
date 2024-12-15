from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    deviceHash: str
    uid: Optional[str]
    confirmed: Optional[bool]
    sendSMS: Optional[bool]
    phoneConfirmed: Optional[bool]


class Panel(BaseModel):
    clearAlarmMessage: str
    poldAlarmName: Optional[str]
    poldAlarmMesage: Optional[str]
    showClearAlarm: bool
    waterOn: bool
    canRecieveCmd: bool
    offline: bool
    tooCold: bool
    poldMissingLabels: bool
    scene: str
    activeScene: str
    flowValue: float
    tripValue: float
    countdownTimer: float
    timeToAlarm: float
    maxTimeValue: float
    updatedDate: str
    totalPold: int
    apiSource: int
    updateInterval: int
    sendCmdMessage: Optional[str]
    poldBatteryLow: bool
    poldAlarmId: Optional[str]
    poldInfoMesage: Optional[str]
    address1: str
    address2: str
    city: str
    state: str
    zip: str
    noDataHistory: bool
    sortOrder: int
    utcDate: str
    standbyMinRemain: float
    standbyMinExhausted: float
    stanbyMinTotal: float
    standbyPctExhausted: float
    canCancelStandby: bool
    waterOnByStandby: bool
    polds: list
    needsUpdate: bool
    needsUpdateMsg: Optional[str]
    hasWiredSensor: bool
    wiredSensorName: Optional[str]
    waterOnLabel: str
    waterOffLabel: str
    alarmAlertMuted: bool
    alarmAlertMutedEnd: Optional[str]
    alarmAlertMuteEndUtc: str
    alarmAlertMuteDuration: Optional[str]
    canMuteAlarmAlert: bool
    canUnMuteAlarmAlert: bool
    batAlertMuted: bool
    batAlertMutedEnd: Optional[str]
    batAlertMuteEndUtc: str
    batAlertMuteDuration: Optional[str]
    schedulingAlartMuted: bool
    schedulingAlartMutedEnd: Optional[str]
    schedulingAlartMutedEndUtc: str
    schedulingAlartMuteDuration: Optional[str]
    deviceOfflineMuted: bool
    deviceOfflineMutedEnd: Optional[str]
    deviceOfflineMuteEndUtc: str
    deviceOfflineMuteDuration: Optional[str]
    coldAlertMuted: bool
    coldAlertMutedEnd: Optional[str]
    coldAlertMuteEndUtc: str
    coldAlertMuteDuration: Optional[str]
    windowsZoneName: str
    ianaZoneName: str
    fallbackScene: Optional[str]
    runningSchedules: int
    schedulingEnabled: bool
    samePoldMute: bool
    b0Set: bool
    shareCount: int
    lastEmail: str
    lastSMS: Optional[str]
    lastPush: str
    id: int
    mainUserId: str
    mainUserEmail: str
    shared: bool
    isLDA: bool
    inAlarm: bool
    alarmType: int
    alarmHeader: Optional[str]
    alarmMessage: str
    infoMesage: str
    textIdentifier: str


class NewFeature(BaseModel):
    name: str
    show: bool


class Customer(BaseModel):
    id: str
    firstName: str
    middleName: Optional[str]
    lastName: str
    phoneNumber: str
    email: str
    pushNotifications: bool
    smsNotifications: bool
    emailNotifications: bool
    phoneNumberConfirmed: bool
    confirmInProgress: int
    additionalUsers: list
    panels: list[Panel]
    allowedFeatures: list[str]
    newFeatures: list[NewFeature]
    requireAcceptTerms: bool
    requireAcceptPrivacy: bool
    showTutorial: bool


class ApiResponse(BaseModel):
    customer: Customer
    iOSVersion: str
    androidVersion: str
    inMaint: str
