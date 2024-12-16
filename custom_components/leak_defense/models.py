"""Models for the Leak Defense API."""

from enum import Enum

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """TokenResponse model."""

    token: str
    device_hash: str = Field(alias="deviceHash")
    uid: str | None
    confirmed: bool | None
    send_sms: bool | None = Field(alias="sendSMS")
    phone_confirmed: bool | None = Field(alias="phoneConfirmed")


class Panel(BaseModel):
    """Panel model."""

    clear_alarm_message: str = Field(alias="clearAlarmMessage")
    pold_alarm_name: str | None = Field(alias="poldAlarmName")
    pold_alarm_message: str | None = Field(alias="poldAlarmMesage")
    show_clear_alarm: bool = Field(alias="showClearAlarm")
    water_on: bool = Field(alias="waterOn")
    can_receive_cmd: bool = Field(alias="canRecieveCmd")
    offline: bool
    too_cold: bool = Field(alias="tooCold")
    pold_missing_labels: bool = Field(alias="poldMissingLabels")
    scene: str
    active_scene: str = Field(alias="activeScene")
    flow_value: float = Field(alias="flowValue")
    trip_value: float = Field(alias="tripValue")
    countdown_timer: float = Field(alias="countdownTimer")
    time_to_alarm: float = Field(alias="timeToAlarm")
    max_time_value: float = Field(alias="maxTimeValue")
    updated_date: str = Field(alias="updatedDate")
    total_pold: int = Field(alias="totalPold")
    api_source: int = Field(alias="apiSource")
    update_interval: int = Field(alias="updateInterval")
    send_cmd_message: str | None = Field(alias="sendCmdMessage")
    pold_battery_low: bool = Field(alias="poldBatteryLow")
    pold_alarm_id: str | None = Field(alias="poldAlarmId")
    pold_info_message: str | None = Field(alias="poldInfoMesage")
    address_1: str = Field(alias="address1")
    address_2: str = Field(alias="address2")
    city: str
    state: str
    zip: str
    no_data_history: bool = Field(alias="noDataHistory")
    sort_order: int = Field(alias="sortOrder")
    utc_date: str = Field(alias="utcDate")
    standby_min_remain: float = Field(alias="standbyMinRemain")
    standby_min_exhausted: float = Field(alias="standbyMinExhausted")
    standby_min_total: float = Field(alias="stanbyMinTotal")
    standby_pct_exhausted: float = Field(alias="standbyPctExhausted")
    can_cancel_standby: bool = Field(alias="canCancelStandby")
    water_on_by_standby: bool = Field(alias="waterOnByStandby")
    polds: list
    needs_update: bool = Field(alias="needsUpdate")
    needs_update_msg: str | None = Field(alias="needsUpdateMsg")
    has_wired_sensor: bool = Field(alias="hasWiredSensor")
    wired_sensor_name: str | None = Field(alias="wiredSensorName")
    water_on_label: str = Field(alias="waterOnLabel")
    water_off_label: str = Field(alias="waterOffLabel")
    alarm_alert_muted: bool = Field(alias="alarmAlertMuted")
    alarm_alert_muted_end: str | None = Field(alias="alarmAlertMutedEnd")
    alarm_alert_mute_end_utc: str = Field(alias="alarmAlertMuteEndUtc")
    alarm_alert_mute_duration: str | None = Field(alias="alarmAlertMuteDuration")
    can_mute_alarm_alert: bool = Field(alias="canMuteAlarmAlert")
    can_unmute_alarm_alert: bool = Field(alias="canUnMuteAlarmAlert")
    bat_alert_muted: bool = Field(alias="batAlertMuted")
    bat_alert_muted_end: str | None = Field(alias="batAlertMutedEnd")
    bat_alert_mute_end_utc: str = Field(alias="batAlertMuteEndUtc")
    bat_alert_mute_duration: str | None = Field(alias="batAlertMuteDuration")
    scheduling_alert_muted: bool = Field(alias="schedulingAlartMuted")
    scheduling_alert_muted_end: str | None = Field(alias="schedulingAlartMutedEnd")
    scheduling_alert_muted_end_utc: str = Field(alias="schedulingAlartMutedEndUtc")
    scheduling_alert_mute_duration: str | None = Field(
        alias="schedulingAlartMuteDuration"
    )
    device_offline_muted: bool = Field(alias="deviceOfflineMuted")
    device_offline_muted_end: str | None = Field(alias="deviceOfflineMutedEnd")
    device_offline_mute_end_utc: str = Field(alias="deviceOfflineMuteEndUtc")
    device_offline_mute_duration: str | None = Field(alias="deviceOfflineMuteDuration")
    cold_alert_muted: bool = Field(alias="coldAlertMuted")
    cold_alert_muted_end: str | None = Field(alias="coldAlertMutedEnd")
    cold_alert_mute_end_utc: str = Field(alias="coldAlertMuteEndUtc")
    cold_alert_mute_duration: str | None = Field(alias="coldAlertMuteDuration")
    windows_zone_name: str = Field(alias="windowsZoneName")
    iana_zone_name: str = Field(alias="ianaZoneName")
    fallback_scene: str | None = Field(alias="fallbackScene")
    running_schedules: int = Field(alias="runningSchedules")
    scheduling_enabled: bool = Field(alias="schedulingEnabled")
    same_pold_mute: bool = Field(alias="samePoldMute")
    b0_set: bool = Field(alias="b0Set")
    share_count: int = Field(alias="shareCount")
    last_email: str = Field(alias="lastEmail")
    last_sms: str | None = Field(alias="lastSMS")
    last_push: str = Field(alias="lastPush")
    id: int
    main_user_id: str = Field(alias="mainUserId")
    main_user_email: str = Field(alias="mainUserEmail")
    shared: bool
    is_lda: bool = Field(alias="isLDA")
    in_alarm: bool = Field(alias="inAlarm")
    alarm_type: int = Field(alias="alarmType")
    alarm_header: str | None = Field(alias="alarmHeader")
    alarm_message: str = Field(alias="alarmMessage")
    info_message: str = Field(alias="infoMesage")
    text_identifier: str = Field(alias="textIdentifier")


class NewFeature(BaseModel):
    """NewFeature model."""

    name: str
    show: bool


class Customer(BaseModel):
    """Customer model."""

    id: str
    first_name: str = Field(alias="firstName")
    middle_name: str | None = Field(alias="middleName")
    last_name: str = Field(alias="lastName")
    phone_number: str = Field(alias="phoneNumber")
    email: str
    push_notifications: bool = Field(alias="pushNotifications")
    sms_notifications: bool = Field(alias="smsNotifications")
    email_notifications: bool = Field(alias="emailNotifications")
    phone_number_confirmed: bool = Field(alias="phoneNumberConfirmed")
    confirm_in_progress: int = Field(alias="confirmInProgress")
    additional_users: list = Field(alias="additionalUsers")
    panels: list[Panel]
    allowed_features: list[str] = Field(alias="allowedFeatures")
    new_features: list[NewFeature] = Field(alias="newFeatures")
    require_accept_terms: bool = Field(alias="requireAcceptTerms")
    require_accept_privacy: bool = Field(alias="requireAcceptPrivacy")
    show_tutorial: bool = Field(alias="showTutorial")


class ApiResponse(BaseModel):
    """ApiResponse model."""

    customer: Customer
    ios_version: str = Field(alias="iOSVersion")
    android_version: str = Field(alias="androidVersion")
    in_maint: str = Field(alias="inMaint")


class LegacyRequest(BaseModel):
    """LegacyRequest model."""

    id: int
    mode: str
    trip_time: str = Field(alias="tripTime")
    trip_val: str = Field(alias="tripVal")
    water_off: bool = Field(alias="waterOff")
    clear_alarm: bool = Field(alias="clearAlarm")


class HexRequest(BaseModel):
    """HexRequest model."""

    Scene: str | None = None
    value: str | None = None


class CommandSetScene(BaseModel):
    """CommandSetScene model."""

    ApiSource: int
    ReturnPanelVM: bool
    LegacyRequest: LegacyRequest
    HexRequest: HexRequest


class SceneEnum(str, Enum):
    """Enum class for the scene attribute of the Panel model."""

    HOME = "HOME"
    AWAY = "AWAY"
    STANDBY = "STANDBY"
