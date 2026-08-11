# 🚀 Complete Properties & Appointments Setup Guide

## 📦 What You're Getting

End-to-end functionality for:
- ✅ **Properties**: Add, Edit, View, Delete
- ✅ **Appointments**: Schedule, View, Complete, Cancel
- ✅ **Modal Forms**: Beautiful HTMX-powered modals
- ✅ **Auto-linking**: Properties ↔ Conversations ↔ Appointments

## 📁 Files to Add

### Backend (app.py)
1. `routes_properties_appointments.py` - All the Flask routes

### Frontend (templates/partials/)
1. `property_form.html` - Add/Edit property modal
2. `property_details.html` - View property details modal
3. `appointment_form.html` - Schedule appointment modal
4. `appointment_details.html` - View appointment details modal

## 🔧 Step-by-Step Installation

### Step 1: Add Backend Routes to app.py

Open your `app.py` and add these routes. You can place them anywhere after your existing routes:

```python
# ================================
# PROPERTIES ROUTES
# ================================

@app.route("/app/dashboard/properties/add", methods=["GET", "POST"])
def property_add():
    """Add new property form and handler"""
    user_id = request.args.get("user_id") or request.form.get("user_id")
    
    if request.method == "POST":
        try:
            property_data = {
                "user_id": user_id,
                "address": request.form.get("address"),
                "property_type": request.form.get("property_type"),
                "bedrooms": int(request.form.get("bedrooms")) if request.form.get("bedrooms") else None,
                "bathrooms": float(request.form.get("bathrooms")) if request.form.get("bathrooms") else None,
                "square_feet": int(request.form.get("square_feet")) if request.form.get("square_feet") else None,
                "price": float(request.form.get("price")) if request.form.get("price") else None,
                "description": request.form.get("description"),
                "amenities": request.form.get("amenities"),
                "availability_status": "available",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            result = supabase.table("properties").insert(property_data).execute()
            
            return """
            <script>
                window.location.reload();
            </script>
            """
        except Exception as e:
            print(f"Error adding property: {e}")
            return jsonify({"error": str(e)}), 500
    
    return render_template("partials/property_form.html", user_id=user_id, mode="add")

# ... (copy all other routes from routes_properties_appointments.py)
```

**OR** Simply copy the entire contents of `routes_properties_appointments.py` and paste it into your `app.py` file.

### Step 2: Add Template Files

Create these files in your `templates/partials/` directory:

```bash
templates/
└── partials/
    ├── property_form.html          # Copy from property_form.html
    ├── property_details.html        # Copy from property_details.html
    ├── appointment_form.html        # Copy from appointment_form.html
    └── appointment_details.html     # Copy from appointment_details.html
```

### Step 3: Verify Database Tables

Make sure these tables exist in Supabase with the correct columns:

**properties table:**
```sql
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    address TEXT NOT NULL,
    property_type TEXT,
    bedrooms INTEGER,
    bathrooms NUMERIC,
    square_feet INTEGER,
    price NUMERIC,
    description TEXT,
    amenities TEXT,
    availability_status TEXT DEFAULT 'available',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
```

**appointments table:**
```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    client_email TEXT NOT NULL,
    client_name TEXT,
    property_id UUID REFERENCES properties(id),
    conversation_id UUID REFERENCES conversations(id),
    appointment_time TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
```

### Step 4: Test Properties Flow

1. **Add Property**:
   - Click "Add Property" button in properties page
   - Fill out the form
   - Submit
   - Property appears in list

2. **View Property**:
   - Click "View" on any property
   - See full details, amenities, activity
   - Click "Edit" to modify

3. **Edit Property**:
   - Change availability status
   - Update price or details
   - Save changes

4. **Delete Property**:
   - View property details
   - Click "Delete Property"
   - Confirm deletion

### Step 5: Test Appointments Flow

1. **Schedule from Dashboard**:
   - Click "Schedule" button in appointments section
   - Select property, date, time
   - Enter client info
   - Submit

2. **Schedule from Conversation**:
   - In conversations page
   - Click "Book Now" on a conversation
   - Form auto-fills client and property
   - Select date/time
   - Submit

3. **View Appointment**:
   - Click on any appointment
   - See full details
   - View related conversation (if any)

4. **Complete Appointment**:
   - Open appointment details
   - Click "Mark as Complete"
   - Status updates to completed

5. **Cancel Appointment**:
   - Open appointment details
   - Click "Cancel Appointment"
   - Status updates to cancelled

## 🔗 How Everything Connects

```
User inquires about property (via email)
    ↓
Conversation created (conversation_stage: initial_inquiry)
    ↓
AI asks for viewing times (conversation_stage: awaiting_availability)
    ↓
Client provides time preference
    ↓
Agent clicks "Book Now" on conversation
    ↓
Appointment form opens (pre-filled with client + property)
    ↓
Agent schedules appointment
    ↓
Conversation updates (conversation_stage: appointment_booked)
    ↓
Appointment appears in dashboard
    ↓
Agent marks as complete after showing
    ↓
Conversation updates (conversation_stage: completed)
```

## 🎨 UI Components Included

### Modals
- ✅ Dark overlay backdrop
- ✅ Click outside to close
- ✅ ESC key to close
- ✅ Smooth animations
- ✅ HTMX-powered (no page refresh)

### Forms
- ✅ Required field validation
- ✅ Proper input types (date, time, email, number)
- ✅ Quick time slot buttons
- ✅ Auto-fill from conversations
- ✅ Responsive design

### Property Cards
- ✅ Status badges (Available, Pending, Rented)
- ✅ Amenity tags
- ✅ Activity timeline
- ✅ Stats grid (bed/bath/sqft/price)

### Appointment Cards
- ✅ Visual date/time display
- ✅ Status badges
- ✅ Client and property info
- ✅ Action buttons

## 🐛 Troubleshooting

### "Template not found" error
**Solution**: Make sure files are in `templates/partials/` directory

### "Column does not exist" error
**Solution**: Check database schema matches the SQL above

### Modal doesn't close
**Solution**: Make sure HTMX script is loaded in dashboard.html

### Form submission doesn't work
**Solution**: Check Flask route is correctly defined and imported

### Properties not showing
**Solution**: Check user_id is being passed correctly to queries

### Appointments not creating
**Solution**: Verify properties table has at least one property

## 📋 Quick Checklist

Backend:
- [ ] Added all routes to app.py
- [ ] Tested routes return 200 (no errors)
- [ ] Database tables exist with correct columns

Frontend:
- [ ] Added 4 template files to partials/
- [ ] HTMX script loaded in dashboard.html
- [ ] CSS variables defined in dashboard.html

Testing:
- [ ] Can add a property
- [ ] Can view property details
- [ ] Can edit a property
- [ ] Can delete a property
- [ ] Can schedule an appointment
- [ ] Can view appointment details
- [ ] Can complete an appointment
- [ ] Can cancel an appointment

## 🎯 Usage Examples

### Add Property Button
```html
<button class="btn btn-primary"
        hx-get="/app/dashboard/properties/add?user_id={{ user_id }}"
        hx-target="body"
        hx-swap="beforeend">
    <i class="fas fa-plus"></i>
    Add Property
</button>
```

### View Property Button
```html
<button class="btn btn-secondary"
        hx-get="/app/dashboard/properties/{{ property.id }}/view?user_id={{ user_id }}"
        hx-target="body"
        hx-swap="beforeend">
    <i class="fas fa-eye"></i>
    View
</button>
```

### Schedule Appointment Button
```html
<button class="btn btn-primary"
        hx-get="/app/dashboard/appointments/new?user_id={{ user_id }}"
        hx-target="body"
        hx-swap="beforeend">
    <i class="fas fa-calendar-plus"></i>
    Schedule
</button>
```

### View Appointment Button
```html
<button class="btn btn-secondary"
        hx-get="/app/dashboard/appointments/{{ apt.id }}?user_id={{ user_id }}"
        hx-target="body"
        hx-swap="beforeend">
    <i class="fas fa-eye"></i>
    View
</button>
```

## 🚀 You're All Set!

Your dashboard now has full CRUD functionality for properties and appointments. The AI email system will automatically create conversations, and you can manually book appointments from those conversations or create them directly.

Everything is connected and working end-to-end! 🎉
