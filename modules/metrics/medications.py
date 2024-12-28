"""
Medications Metrics Blueprint for the Healthsome application.

This module provides functionality for managing medication records,
including listing, creating, editing, deleting, toggling medication statuses,
and filtering records by date range.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from helpers.db_helpers import query_db, execute_db
from helpers.datetime_helpers import calculate_date_range

bp = Blueprint('medications', __name__, url_prefix='/medications')

@bp.route('/')
def list_records():
    """
    Display a list of medication records for the logged-in user based on selected date range.

    Returns:
        str: Rendered template with records or redirect to login page if not logged in.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your records.", "error")
        return redirect(url_for('auth.login'))

    range_option = request.args.get('range', 'last_week')  # Default to 'last_week'
    start_date, end_date = calculate_date_range(range_option)

    query = "SELECT * FROM medications WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date_time BETWEEN ? AND ? ORDER BY date_time DESC"
        params.extend([start_date, end_date])
    else:
        query += " ORDER BY date_time DESC"

    records = query_db(query, params)
    return render_template('metrics/medications/list.html', records=records, range_option=range_option)

@bp.route('/create', methods=['GET', 'POST'])
def create_record():
    """
    Create a new medication record for the logged-in user.

    Returns:
        str: Rendered template or redirect to record list on success.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to add a record.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        date_time = request.form['date_time'].replace('T', ' ')
        medication_name = request.form['medication_name']
        dosage = request.form['dosage']
        taken = request.form.get('taken', '0')

        try:
            execute_db(
                "INSERT INTO medications (date_time, medication_name, dosage, taken, user_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (date_time, medication_name, dosage, int(taken), user_id)
            )
            flash("Record added successfully.", "success")
            return redirect(url_for('medications.list_records'))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template('metrics/medications/create.html', current_time=current_time)

@bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    """
    Edit an existing medication record for the logged-in user.

    Args:
        record_id (int): ID of the record to edit.

    Returns:
        str: Rendered template or redirect to record list on success.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to edit a record.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        date_time = request.form['date_time'].replace('T', ' ')
        medication_name = request.form['medication_name']
        dosage = request.form['dosage']
        taken = request.form.get('taken', '0')

        try:
            execute_db(
                "UPDATE medications SET date_time = ?, medication_name = ?, dosage = ?, taken = ? "
                "WHERE id = ? AND user_id = ?",
                (date_time, medication_name, dosage, int(taken), record_id, user_id)
            )
            flash("Record updated successfully.", "success")
            return redirect(url_for('medications.list_records'))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    record = query_db("SELECT * FROM medications WHERE id = ? AND user_id = ?",
                      (record_id, user_id), one=True)
    if not record:
        flash("Record not found.", "error")
        return redirect(url_for('medications.list_records'))

    return render_template('metrics/medications/edit.html', record=record)

@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """
    Delete a medication record for the logged-in user.

    Args:
        record_id (int): ID of the record to delete.

    Returns:
        str: Redirect to record list.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to delete a record.", "error")
        return redirect(url_for('auth.login'))

    try:
        execute_db("DELETE FROM medications WHERE id = ? AND user_id = ?", (record_id, user_id))
        flash("Record deleted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for('medications.list_records'))

@bp.route('/toggle/<int:record_id>', methods=['POST'])
def toggle_taken(record_id):
    """
    Toggle the "taken" status of a medication record.

    Args:
        record_id (int): ID of the record to toggle.

    Returns:
        str: Redirect to record list.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to change medication status.", "error")
        return redirect(url_for('auth.login'))

    record = query_db("SELECT taken FROM medications WHERE id = ? AND user_id = ?",
                      (record_id, user_id), one=True)
    if not record:
        flash("Record not found.", "error")
        return redirect(url_for('medications.list_records'))

    new_status = 0 if record['taken'] else 1
    try:
        execute_db("UPDATE medications SET taken = ? WHERE id = ? AND user_id = ?",
                   (new_status, record_id, user_id))
        flash("Medication status updated successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for('medications.list_records'))

@bp.route('/data')
def medications_data():
    """
    Return medication data as JSON for the chart, filtered by the selected date range.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    range_option = request.args.get('range', 'last_week')  # Default to 'last_week'
    start_date, end_date = calculate_date_range(range_option)

    query = "SELECT date_time, medication_name, taken FROM medications WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date_time BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY date_time ASC"

    records = query_db(query, params)
    return jsonify([
        {
            "date": record["date_time"],
            "medication": record["medication_name"],
            "status": "Taken" if record["taken"] else "Missed"
        }
        for record in records
    ])
