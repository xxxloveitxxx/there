# Add these routes to your app.py

from datetime import datetime, timedelta, timezone
from flask import request, render_template, jsonify

# ================================
# PROPERTIES ROUTES
# ================================

@app.route("/app/dashboard/properties/add", methods=["GET", "POST"])
def property_add():
    """Add new property form and handler"""
    user_id = request.args.get("user_id") or request.form.get("user_id")
    
    if request.method == "POST":
        try:
            # Get form data
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
            
            # Insert into database
            result = supabase.table("properties").insert(property_data).execute()
            
            if result.data:
                # Return success and trigger refresh
                return """
                <script>
                    window.location.reload();
                </script>
                """
            else:
                return jsonify({"error": "Failed to add property"}), 500
                
        except Exception as e:
            print(f"Error adding property: {e}")
            return jsonify({"error": str(e)}), 500
    
    # GET request - show form
    return render_template("partials/property_form.html", user_id=user_id, mode="add")


@app.route("/app/dashboard/properties/<property_id>/edit", methods=["GET", "POST"])
def property_edit(property_id):
    """Edit existing property"""
    user_id = request.args.get("user_id") or request.form.get("user_id")
    
    if request.method == "POST":
        try:
            # Update property
            update_data = {
                "address": request.form.get("address"),
                "property_type": request.form.get("property_type"),
                "bedrooms": int(request.form.get("bedrooms")) if request.form.get("bedrooms") else None,
                "bathrooms": float(request.form.get("bathrooms")) if request.form.get("bathrooms") else None,
                "square_feet": int(request.form.get("square_feet")) if request.form.get("square_feet") else None,
                "price": float(request.form.get("price")) if request.form.get("price") else None,
                "description": request.form.get("description"),
                "amenities": request.form.get("amenities"),
                "availability_status": request.form.get("availability_status", "available"),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            result = supabase.table("properties") \
                .update(update_data) \
                .eq("id", property_id) \
                .eq("user_id", user_id) \
                .execute()
            
            return """
            <script>
                window.location.reload();
            </script>
            """
            
        except Exception as e:
            print(f"Error updating property: {e}")
            return jsonify({"error": str(e)}), 500
    
    # GET request - show form with existing data
    property_data = supabase.table("properties") \
        .select("*") \
        .eq("id", property_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute().data
    
    return render_template(
        "partials/property_form.html",
        user_id=user_id,
        mode="edit",
        property=property_data
    )


@app.route("/app/dashboard/properties/<property_id>/view")
def property_view(property_id):
    """View property details"""
    user_id = request.args.get("user_id")
    
    # Get property with related data
    property_data = supabase.table("properties") \
        .select("*") \
        .eq("id", property_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute().data
    
    # Get conversations/inquiries for this property
    conversations = supabase.table("conversations") \
        .select("*") \
        .eq("property_id", property_id) \
        .execute().data or []
    
    # Get appointments for this property
    appointments = supabase.table("appointments") \
        .select("*") \
        .eq("property_id", property_id) \
        .order("appointment_time", desc=False) \
        .execute().data or []
    
    return render_template(
        "partials/property_details.html",
        user_id=user_id,
        property=property_data,
        conversations=conversations,
        appointments=appointments
    )


@app.route("/app/dashboard/properties/<property_id>/delete", methods=["POST"])
def property_delete(property_id):
    """Delete a property"""
    user_id = request.form.get("user_id")
    
    try:
        supabase.table("properties") \
            .delete() \
            .eq("id", property_id) \
            .eq("user_id", user_id) \
            .execute()
        
        return """
        <script>
            window.location.reload();
        </script>
        """
    except Exception as e:
        print(f"Error deleting property: {e}")
        return jsonify({"error": str(e)}), 500


# ================================
# APPOINTMENTS ROUTES
# ================================

@app.route("/app/dashboard/appointments/new", methods=["GET", "POST"])
def appointment_new():
    """Create new appointment"""
    user_id = request.args.get("user_id") or request.form.get("user_id")
    conversation_id = request.args.get("conversation_id")
    
    if request.method == "POST":
        try:
            # Parse appointment date and time
            date_str = request.form.get("date")
            time_str = request.form.get("time")
            
            # Combine date and time
            appointment_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            appointment_data = {
                "user_id": user_id,
                "client_email": request.form.get("client_email"),
                "client_name": request.form.get("client_name"),
                "property_id": request.form.get("property_id") or None,
                "conversation_id": request.form.get("conversation_id") or None,
                "appointment_time": appointment_datetime.isoformat(),
                "duration_minutes": 30,
                "status": "scheduled",
                "notes": request.form.get("notes"),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            result = supabase.table("appointments").insert(appointment_data).execute()
            
            # If there's a conversation, update it
            if conversation_id:
                supabase.table("conversations") \
                    .update({
                        "conversation_stage": "appointment_booked",
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }) \
                    .eq("id", conversation_id) \
                    .execute()
            
            return """
            <script>
                window.location.reload();
            </script>
            """
            
        except Exception as e:
            print(f"Error creating appointment: {e}")
            return jsonify({"error": str(e)}), 500
    
    # GET request - show form
    # Get user's properties for dropdown
    properties = supabase.table("properties") \
        .select("id, address") \
        .eq("user_id", user_id) \
        .eq("availability_status", "available") \
        .execute().data or []
    
    # If conversation_id provided, get conversation details
    conversation = None
    if conversation_id:
        conversation = supabase.table("conversations") \
            .select("*, properties(address)") \
            .eq("id", conversation_id) \
            .single() \
            .execute().data
    
    return render_template(
        "partials/appointment_form.html",
        user_id=user_id,
        mode="new",
        properties=properties,
        conversation=conversation
    )


@app.route("/app/dashboard/appointments/<appointment_id>")
def appointment_view(appointment_id):
    """View appointment details"""
    user_id = request.args.get("user_id")
    
    appointment = supabase.table("appointments") \
        .select("*, properties(address), conversations(*)") \
        .eq("id", appointment_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute().data
    
    return render_template(
        "partials/appointment_details.html",
        user_id=user_id,
        appointment=appointment
    )


@app.route("/app/dashboard/appointments/<appointment_id>/complete", methods=["POST"])
def appointment_complete(appointment_id):
    """Mark appointment as complete"""
    user_id = request.form.get("user_id")
    
    try:
        # Update appointment status
        supabase.table("appointments") \
            .update({
                "status": "completed",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }) \
            .eq("id", appointment_id) \
            .eq("user_id", user_id) \
            .execute()
        
        # Get the appointment to update conversation
        apt = supabase.table("appointments") \
            .select("conversation_id") \
            .eq("id", appointment_id) \
            .single() \
            .execute().data
        
        # Update conversation to completed if exists
        if apt and apt.get("conversation_id"):
            supabase.table("conversations") \
                .update({
                    "conversation_stage": "completed",
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }) \
                .eq("id", apt["conversation_id"]) \
                .execute()
        
        return """
        <script>
            window.location.reload();
        </script>
        """
        
    except Exception as e:
        print(f"Error completing appointment: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/app/dashboard/appointments/<appointment_id>/cancel", methods=["POST"])
def appointment_cancel(appointment_id):
    """Cancel an appointment"""
    user_id = request.form.get("user_id")
    
    try:
        supabase.table("appointments") \
            .update({
                "status": "cancelled",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }) \
            .eq("id", appointment_id) \
            .eq("user_id", user_id) \
            .execute()
        
        return """
        <script>
            window.location.reload();
        </script>
        """
        
    except Exception as e:
        print(f"Error cancelling appointment: {e}")
        return jsonify({"error": str(e)}), 500
