"""
Weight Metrics Blueprint for the Healthsome application.

This module provides functionality for managing weight records,
including listing, creating, editing, deleting, and filtering records by date range.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from helpers.db_helpers import query_db, execute_db
from helpers.datetime_helpers import calculate_date_range

bp = Blueprint('weight', __name__, url_prefix='/weight')

@bp.route('/')
def list_records():
    """
    Display a list of weight records for the logged-in user based on selected date range.

    Returns:
        str: Rendered template with records or redirect to login page if not logged in.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your records.", "error")
        return redirect(url_for('auth.login'))

    range_option = request.args.get('range', 'last_week')  # Default to 'last_week'
    start_date, end_date = calculate_date_range(range_option)

    query = "SELECT * FROM weight WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date_time BETWEEN ? AND ? ORDER BY date_time DESC"
        params.extend([start_date, end_date])
    else:
        query += " ORDER BY date_time DESC"

    records = query_db(query, params)
    return render_template('metrics/weight/list.html', records=records, range_option=range_option)


@bp.route('/create', methods=['GET', 'POST'])
def create_record():
    """
    Create a new weight record for the logged-in user.

    Returns:
        str: Rendered template or redirect to record list on success.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to add a record.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        date_time = request.form['date_time'].replace('T', ' ')
        weight_value = request.form['weight_value']

        try:
            execute_db(
                "INSERT INTO weight (date_time, weight_value, user_id) VALUES (?, ?, ?)",
                (date_time, weight_value, user_id)
            )
            flash("Record added successfully.", "success")
            return redirect(url_for('weight.list_records'))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template('metrics/weight/create.html', current_time=current_time)

@bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    """
    Edit an existing weight record for the logged-in user.

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
        weight_value = request.form['weight_value']

        try:
            execute_db(
                "UPDATE weight SET date_time = ?, weight_value = ? WHERE id = ? AND user_id = ?",
                (date_time, weight_value, record_id, user_id)
            )
            flash("Record updated successfully.", "success")
            return redirect(url_for('weight.list_records'))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    record = query_db("SELECT * FROM weight WHERE id = ? AND user_id = ?",
                      (record_id, user_id), one=True)
    if not record:
        flash("Record not found.", "error")
        return redirect(url_for('weight.list_records'))

    return render_template('metrics/weight/edit.html', record=record)

@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """
    Delete a weight record for the logged-in user.

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
        execute_db("DELETE FROM weight WHERE id = ? AND user_id = ?", (record_id, user_id))
        flash("Record deleted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for('weight.list_records'))

@bp.route('/data')
def weight_data():
    """
    Return weight data as JSON for the chart, filtered by the selected date range.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    range_option = request.args.get('range', 'last_week')  # Default to 'last_week'
    start_date, end_date = calculate_date_range(range_option)

    query = "SELECT date_time, weight_value FROM weight WHERE user_id = ?"
    params = [user_id]

    if start_date:
        query += " AND date_time BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY date_time ASC"

    records = query_db(query, params)
    return jsonify([
        {"date": record["date_time"], "weight": record["weight_value"]}
        for record in records
    ])
