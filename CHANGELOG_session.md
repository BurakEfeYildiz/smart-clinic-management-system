# Session Changelog

## [2026-05-02]

---

### Feature: F3 — Patient Flow Tracking

**Files Modified:** `clinic/services/patient_flow_service.py`, `templates/patient_flow/index.html`

**Modified:**
- `ALLOWED_TRANSITIONS` genişletildi: `waiting → in_consultation → assessment → done` (+ cancelled her aşamada)
- `update_status()`: yeni statüler için `started_at`, `completed_at`, `appointment.status` sync eklendi
- Gecikmiş hasta tespiti: `was_delayed` bayrağı `in_consultation` geçişinde kontrol edilip staff bildirimi tetikleniyor
- Template: her statüsün butonları ayrı ayrı gösteriliyor (Start Consultation, Send to Assessment, Complete Visit, Cancel Visit)
- Template: queue satırına badge ve gecikme göstergesi eklendi

**Reason:** Mevcut `waiting → in_exam → completed` zinciri eksikti; `assessment` aşaması yoktu.

---

### Feature: F6 — Queue Management and Prioritization

**Files Modified:** `clinic/models/patient_flow.py`, `clinic/repositories/clinic_repository.py`,
`clinic/services/appointment_service.py`, `clinic/controllers/appointments.py`,
`templates/appointments/index.html`, `templates/patient_flow/index.html`,
`static/css/styles.css`

**Added:**
- `PatientFlow.priority` kolonu (0=Normal, 1=Urgent, 2=Emergency)
- `PatientFlow.is_delayed` property: randevu saatinden 15 dk sonra hâlâ bekliyor ise True
- `PatientFlow.priority_label` property
- `list_patient_flow()`: `priority DESC, queue_number ASC` sıralamaya geçildi; `active_only` ve `today_only` parametreleri eklendi
- `check_in_appointment(priority=0)`: priority parametresi alıyor
- Check-in formuna priority select dropdown eklendi
- CSS: `.badge`, `.badge.emergency`, `.badge.urgent`, `.badge.delay`, `.btn-danger`, `.stat-grid`, `.stat-card`, `.flow-card.delayed` sınıfları

**Reason:** FIFO kuyruk önceliklendirmeyi desteklemiyordu; acil vakalar sıranın başına geçemiyordu.

---

### Feature: F1 — Patient Appointment Management (Cancel + Reschedule)

**Files Modified:** `clinic/services/appointment_service.py`, `clinic/controllers/appointments.py`,
`templates/appointments/index.html`

**Created:** `templates/appointments/reschedule.html`

**Added:**
- `AppointmentService.cancel_appointment()`: yetki kontrolü (hasta sadece kendi randevusunu iptal edebilir), flow_record güncelleme, bildirim
- `AppointmentService.reschedule_appointment()`: slot çakışma kontrolü, uygunluk kontrolü, bildirim
- Route `POST /appointments/<id>/cancel`
- Route `GET+POST /appointments/<id>/reschedule` — slot seçim arayüzü ile
- Appointments listesine Reschedule + Cancel butonları eklendi

**Reason:** Sadece randevu oluşturma mevcuttu; iptal ve yeniden zamanlama tamamen eksikti.

---

### Feature: F2 — Doctor Availability Management (Delete)

**Files Modified:** `clinic/services/availability_service.py`, `clinic/controllers/availability.py`,
`templates/availability/index.html`

**Added:**
- `AvailabilityService.delete_availability()`: aktif randevu çakışması varsa silmeyi bloklar
- Route `POST /availability/<id>/delete`
- `ClinicRepository.get_availability()`, `delete_availability()` metodları
- Template: her uygunluk girişinin yanına Delete butonu eklendi

**Reason:** Doktor mevcut girişleri silemiyordu; sadece ekleme vardı.

---

### Feature: F8 — Notifications and Alerts

**Files Created:** `clinic/models/notification.py`, `clinic/services/notification_service.py`,
`clinic/controllers/notifications.py`, `templates/notifications/index.html`

**Files Modified:** `clinic/models/__init__.py`, `clinic/services/__init__.py`,
`clinic/__init__.py`, `templates/base.html`

**Added:**
- `Notification` modeli: `notifications` tablosu (recipient_user_id, patient_id, title, body, category, is_read)
- `NotificationService`: `notify_patient()`, `notify_staff()`, `notify_user()`, `get_unread_count()`, `mark_all_read()`
- Repository: `add_notification()`, `count_unread_notifications()`, `list_notifications()`, `mark_notifications_read()`
- Context processor: `unread_notifications` değeri tüm template'lerde mevcut
- Nav'da bildirim sayacı badge'i
- Tetikleyiciler: randevu oluşturma, iptal, yeniden zamanlama → hasta bildirimi; gecikmiş hasta konsültasyona girince → staff bildirimi
- CSS: `.notif-badge`, `.notif-item`, `.notif-item.notif-alert/warning/info`

**Reason:** Hiç bildirim sistemi yoktu.

---

### Feature: F4 — Reception Desk Dashboard

**Files Modified:** `clinic/controllers/dashboard.html`, `templates/dashboard/secretary.html`

**Modified:**
- `dashboard.index`: sekreter rolü için `appointments_today`, `flow_items`, `stats` verisi hazırlanıp template'e gönderiliyor
- `secretary.html`: stats bar (Total/Scheduled/In Progress/Done/Cancelled), canlı kuyruk grid'i, bugünün randevu tablosu, inline check-in + priority select

**Reason:** Sekreter dashboard'u sadece navigasyon kartlarından oluşuyordu; hiç gerçek veri yoktu.

---

### Feature: F5 — Doctor Session Dashboard

**Files Modified:** `clinic/controllers/dashboard.py`, `templates/dashboard/doctor.html`

**Modified:**
- `dashboard.index`: doktor rolü için `appointments_today`, `current_patient`, `next_patient`, `stats` verisi
- `doctor.html`: stats bar, "Currently in consultation" paneli (Assessment / Complete aksiyonları), "Next patient" paneli (Call Patient aksiyonu), bugünün tam liste tablosu

**Reason:** Doktor dashboard'u da sadece navigasyon kartlarından oluşuyordu.

---

### Feature: F7 — Administrative Reporting

**Files Created:** `clinic/services/report_service.py`, `clinic/controllers/reports.py`,
`templates/reports/index.html`

**Files Modified:** `clinic/repositories/clinic_repository.py`, `clinic/services/__init__.py`,
`clinic/__init__.py`, `templates/base.html`

**Added:**
- `ReportService`: `appointment_volume()`, `workload_by_department()`, `average_wait_time_minutes()`, `no_show_rate()`
- Repository: `list_appointments_in_range()`, `list_flow_in_range()` tarih aralığı sorguları
- Route `GET /reports/` — başlangıç/bitiş tarihi filtresi, tüm metrikler
- Template: filtre formu, özet stat kartları, doktora göre tablo, departmana göre tablo
- Nav'daki "Reports" butonu gerçek route'a bağlandı

**Reason:** Reports tamamen eksikti; nav'da data-not-implemented butonuydu.

---

### Genel Altyapı Değişiklikleri

**Files Modified:** `clinic/__init__.py`, `clinic/cli.py`, `clinic/models/__init__.py`,
`clinic/services/__init__.py`, `static/css/styles.css`

**Added:**
- `reports_bp` ve `notifications_bp` blueprint kayıtları
- `inject_unread_notifications` context processor
- `cli.py`: demo hesap bilgileri print ediliyor
- CSS: yeni statü renkleri (`in_consultation`, `assessment`, `done`), dashboard bileşenleri

---

## ⚠️ Veritabanı Güncelleme Gerekli

`patient_flow` tablosuna `priority` kolonu ve `notifications` tablosu eklendi.
Projenin virtual environment'ını aktifleştirip şunu çalıştırın:

```bash
flask init-db
```

> Bu komut tüm tabloları siler ve yeniden oluşturur. Demo veriler otomatik yüklenir.
> Demo hesaplar: `secretary@clinic.local` / `doctor@clinic.local` / `patient@clinic.local`
> Şifre: `clinic123`
