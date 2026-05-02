# Session Changelog — 2026-05-02

Bu dosya, oturumda yapılan tüm değişiklikleri kapsamaktadır.

---

## F3 — Patient Flow Tracking (Status Machine Genişletme)

**Değişen Dosyalar:** `clinic/services/patient_flow_service.py`, `templates/patient_flow/index.html`

**Eklendi:**
- `ALLOWED_TRANSITIONS` güncellendi: `waiting → in_consultation → assessment → done` (+ her aşamada `cancelled`)
- `update_status()`: yeni statüler için `started_at`, `completed_at`, `appointment.status` sync
- Gecikme tespiti: `was_delayed` bayrağı `in_consultation` geçişinde kontrol edilip staff bildirimi tetikliyor
- Template: her statüse özel butonlar (Start Consultation, Send to Assessment, Complete Visit, Cancel Visit)
- Template: queue satırına priority badge ve gecikme göstergesi eklendi

**Neden:** Mevcut `waiting → in_exam → completed` zinciri eksikti; `assessment` aşaması yoktu.

---

## F6 — Queue Management and Prioritization

**Değişen Dosyalar:** `clinic/models/patient_flow.py`, `clinic/repositories/clinic_repository.py`, `clinic/services/appointment_service.py`, `clinic/controllers/appointments.py`, `templates/appointments/index.html`, `templates/patient_flow/index.html`, `static/css/styles.css`

**Eklendi:**
- `PatientFlow.priority` kolonu: 0=Normal, 1=Urgent, 2=Emergency
- `PatientFlow.is_delayed` property: randevu saatinden 15 dk sonra hâlâ bekliyorsa `True`
- `PatientFlow.priority_label` property
- `list_patient_flow()`: `priority DESC, queue_number ASC` sıralaması; `active_only` ve `today_only` parametreleri
- `check_in_appointment(priority=0)`: priority parametresi
- Check-in formuna priority select dropdown eklendi
- CSS: `.badge`, `.badge.emergency`, `.badge.urgent`, `.badge.delay`, `.btn-danger`, `.stat-grid`, `.stat-card`, `.flow-card.delayed` sınıfları

**Neden:** FIFO kuyruk önceliklendirmeyi desteklemiyordu.

---

## F1 — Patient Appointment Management (Cancel + Reschedule)

**Değişen Dosyalar:** `clinic/services/appointment_service.py`, `clinic/controllers/appointments.py`, `templates/appointments/index.html`

**Yeni Dosyalar:** `templates/appointments/reschedule.html`

**Eklendi:**
- `AppointmentService.cancel_appointment()`: yetki kontrolü, flow_record güncelleme, bildirim tetikleme
- `AppointmentService.reschedule_appointment()`: slot çakışma + uygunluk kontrolü, bildirim
- Route `POST /appointments/<id>/cancel`
- Route `GET+POST /appointments/<id>/reschedule` — slot seçim arayüzü
- Appointments listesine Reschedule + Cancel butonları eklendi

**Neden:** Sadece randevu oluşturma mevcuttu; iptal ve yeniden zamanlama tamamen eksikti.

---

## F2 — Doctor Availability Management (Delete)

**Değişen Dosyalar:** `clinic/services/availability_service.py`, `clinic/controllers/availability.py`, `templates/availability/index.html`

**Eklendi:**
- `AvailabilityService.delete_availability()`: aktif randevu varsa silmeyi bloklar
- Route `POST /availability/<id>/delete`
- `ClinicRepository.get_availability()`, `delete_availability()` metodları
- Template: her satıra Delete butonu eklendi

**Neden:** Doktor mevcut uygunluk girişlerini silemiyordu.

---

## F4 — Reception Desk Dashboard

**Değişen Dosyalar:** `clinic/controllers/dashboard.py`, `templates/dashboard/secretary.html`

**Eklendi:**
- `dashboard.index`: sekreter için `appointments_today`, `flow_items`, `stats` verisi hazırlanıp template'e gönderildi
- `secretary.html`: stats bar (Total/Scheduled/In Progress/Done/Cancelled), canlı kuyruk grid'i, bugünün randevu tablosu, inline check-in + priority select

**Neden:** Sekreter dashboard'u sadece navigasyon kartlarından oluşuyordu; hiç gerçek veri yoktu.

---

## F5 — Doctor Session Dashboard

**Değişen Dosyalar:** `clinic/controllers/dashboard.py`, `templates/dashboard/doctor.html`

**Eklendi:**
- `dashboard.index`: doktor için `appointments_today`, `current_patient`, `next_patient`, `stats` verisi
- `doctor.html`: stats bar, "Currently in consultation" paneli (Assessment/Complete aksiyonları), "Next patient" paneli (Call Patient aksiyonu), bugünün tam liste tablosu

**Neden:** Doktor dashboard'u da sadece navigasyon kartlarından oluşuyordu.

---

## F7 — Administrative Reporting

**Yeni Dosyalar:** `clinic/services/report_service.py`, `clinic/controllers/reports.py`, `templates/reports/index.html`

**Değişen Dosyalar:** `clinic/repositories/clinic_repository.py`, `clinic/services/__init__.py`, `clinic/__init__.py`, `templates/base.html`

**Eklendi:**
- `ReportService`: `appointment_volume()`, `workload_by_department()`, `average_wait_time_minutes()`, `no_show_rate()`
- Repository: `list_appointments_in_range()`, `list_flow_in_range()` tarih aralığı sorguları
- Route `GET /reports/` — tarih filtresi, tüm metrikler
- Template: filtre formu, özet stat kartları, doktora göre tablo, departmana göre tablo
- Nav'daki "Reports" butonu gerçek route'a bağlandı

**Neden:** Reports tamamen eksikti.

---

## F8 — Notifications and Alerts

**Yeni Dosyalar:** `clinic/models/notification.py`, `clinic/services/notification_service.py`, `clinic/controllers/notifications.py`, `templates/notifications/index.html`

**Değişen Dosyalar:** `clinic/models/__init__.py`, `clinic/services/__init__.py`, `clinic/__init__.py`, `templates/base.html`

**Eklendi:**
- `Notification` modeli: `notifications` tablosu (recipient_user_id, patient_id, title, body, category, is_read)
- `NotificationService`: `notify_patient()`, `notify_staff()`, `notify_user()`, `get_unread_count()`, `mark_all_read()`
- Repository: `add_notification()`, `count_unread_notifications()`, `list_notifications()`, `mark_notifications_read()`
- Context processor: `unread_notifications` tüm template'lerde mevcut
- Nav'da okunmamış bildirim sayacı (kırmızı badge)
- Tetikleyiciler: randevu oluşturma/iptal/yeniden zamanlama → hasta bildirimi; gecikmiş hasta konsültasyona girince → staff bildirimi
- CSS: `.notif-badge`, `.notif-item`, `.notif-item.notif-alert/warning/info`

**Neden:** Hiç bildirim sistemi yoktu.

---

## Genel Altyapı

**Değişen Dosyalar:** `clinic/__init__.py`, `clinic/repositories/clinic_repository.py`, `clinic/models/__init__.py`, `clinic/services/__init__.py`, `static/css/styles.css`

**Eklendi:**
- `reports_bp` ve `notifications_bp` blueprint kayıtları
- `inject_unread_notifications` context processor
- CSS: yeni statü renkleri (`in_consultation`, `assessment`, `done`), dashboard bileşenleri (`.stat-grid`, `.stat-card`, `.queue-row`, `.appt-time`, `.current-patient`)

---

## Demo Data Genişletme

**Değişen Dosya:** `clinic/cli.py`

**Eklendi:**
- 5 departman: Cardiology, Dermatology, Neurology, Orthopedics, Pediatrics
- 5 doktor (her departmanda bir tane)
- 2 sekreter
- 6 hasta (user hesabı + patient kaydı)
- 6 örnek randevu (bugün için)
- Her doktor için 7 günlük uygunluk (09:00–17:00, 30 dk slot)
- Tüm şifreler: `clinic123`

---

## Ana Sayfa Düzeltmesi

**Değişen Dosya:** `templates/public/home.html`

**Değiştirildi:**
- "Open Patient Portal" butonu → Login sayfasına yönlendiren `<a>` linki
- "Book Appointment" butonu → Register sayfasına yönlendiren `<a>` linki

**Neden:** İki buton da `data-not-implemented` olarak bırakılmıştı.

---

## Özet — Değişen / Oluşturulan Dosyalar

### Yeni Oluşturulan (10 dosya)
| Dosya | Amaç |
|-------|-------|
| `clinic/models/notification.py` | F8 — Bildirim modeli |
| `clinic/services/notification_service.py` | F8 — Bildirim servisi |
| `clinic/services/report_service.py` | F7 — Raporlama servisi |
| `clinic/controllers/notifications.py` | F8 — Bildirimler controller |
| `clinic/controllers/reports.py` | F7 — Raporlar controller |
| `templates/appointments/reschedule.html` | F1 — Randevu yeniden zamanlama |
| `templates/notifications/index.html` | F8 — Bildirimler sayfası |
| `templates/reports/index.html` | F7 — Raporlar sayfası |
| `CHANGELOG_session.md` | Bu dosya |

### Güncellenen (19 dosya)
| Dosya | Değişen Özellikler |
|-------|-------------------|
| `clinic/__init__.py` | F7, F8 blueprint + context processor |
| `clinic/cli.py` | Demo data genişletme |
| `clinic/models/__init__.py` | F8 Notification eklendi |
| `clinic/models/patient_flow.py` | F6 priority + is_delayed |
| `clinic/repositories/clinic_repository.py` | F1,F2,F4,F6,F7,F8 yeni metodlar |
| `clinic/services/__init__.py` | F7,F8 yeni servisler |
| `clinic/services/appointment_service.py` | F1 cancel/reschedule, F6 priority, F8 bildirim |
| `clinic/services/availability_service.py` | F2 delete |
| `clinic/services/patient_flow_service.py` | F3 yeni status machine |
| `clinic/controllers/appointments.py` | F1 cancel/reschedule, F6 priority |
| `clinic/controllers/availability.py` | F2 delete route |
| `clinic/controllers/dashboard.py` | F4 sekreter, F5 doktor dashboard verisi |
| `clinic/controllers/patient_flow.py` | F6 today_only |
| `static/css/styles.css` | F3,F6,F8 yeni CSS sınıfları |
| `templates/appointments/index.html` | F1 cancel/reschedule, F6 priority |
| `templates/availability/index.html` | F2 delete butonu |
| `templates/base.html` | F7,F8 nav linkleri + bildirim badge |
| `templates/dashboard/doctor.html` | F5 doktor session dashboard |
| `templates/dashboard/secretary.html` | F4 sekreter dashboard |
| `templates/patient_flow/index.html` | F3 yeni statüler, F6 priority badge |
| `templates/public/home.html` | Ana sayfa buton düzeltmesi |
