using Microsoft.AspNetCore.Mvc;
using Npgsql;
using System;
using System.Collections.Generic;
using System.Linq;


[ApiController]
[Route("api/[controller]")]
public class BookingsController : Controller
{
    private readonly string _connectionString = "Host=localhost;Port=5432;Database=BeautySite;Username=postgres;Password=nika11";

    [HttpPost("admin/login")]
    public IActionResult LoginAdmin([FromBody] AdminLoginDto adminLogin)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        connection.Open();

        string query = "SELECT password_hash FROM admins WHERE username = @username";
        using var command = new NpgsqlCommand(query, connection);
        command.Parameters.AddWithValue("username", adminLogin.Username);

        var storedPassword = command.ExecuteScalar()?.ToString();

        if (storedPassword == null || storedPassword != adminLogin.Password)
        {
            return Unauthorized(new { message = "Неправильне ім'я користувача або пароль" });
        }

        return Ok(new { message = "Успішний вхід" });
    }


    public class AdminLoginDto
    {
        public string Username { get; set; }
        public string Password { get; set; }
    }

    [HttpGet("admin/appointments")] 
    public IActionResult GetAllAppointments()
    {
        using var connection = new NpgsqlConnection(_connectionString);
        connection.Open();

        
        string query = @"
        SELECT a.appointment_id, a.customer_id, a.service, a.appointment_time, c.name AS customer_name
        FROM appointments a
        JOIN customers c ON a.customer_id = c.customer_id";

        using var command = new NpgsqlCommand(query, connection);
        using var reader = command.ExecuteReader();

        var appointments = new List<object>();
        while (reader.Read())
        {
            appointments.Add(new
            {
                AppointmentId = reader.GetInt32(0),
                CustomerId = reader.GetInt32(1),
                Service = reader.GetString(2),
                AppointmentTime = reader.GetDateTime(3),
                CustomerName = reader.GetString(4) 
            });
        }

        return Ok(appointments);
    }


    [HttpGet("admin/users")] 
    public IActionResult GetAllUsers()
    {
        using var connection = new NpgsqlConnection(_connectionString);
        connection.Open();

        string query = "SELECT customer_id, name, phone FROM customers"; 
        using var command = new NpgsqlCommand(query, connection);
        using var reader = command.ExecuteReader();

        var users = new List<object>();
        while (reader.Read())
        {
            users.Add(new
            {
                CustomerId = reader.GetInt32(0),
                Name = reader.GetString(1),
                Phone = reader.GetString(2)
            });
        }

        return Ok(users);
    }


    [HttpDelete("admin/appointments/{appointmentId}")] 
    public IActionResult DeleteAppointment(int appointmentId)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        connection.Open();

        string query = "DELETE FROM appointments WHERE appointment_id = @appointmentId";
        using var command = new NpgsqlCommand(query, connection);
        command.Parameters.AddWithValue("appointmentId", appointmentId);

        try
        {
            int affectedRows = command.ExecuteNonQuery();
            if (affectedRows == 0)
            {
                return NotFound(new { message = "Запис не знайдений." });
            }

            return Ok(new { message = "Запис успішно видалено." });
        }
        catch (Exception ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpGet("admin/panel")]
    public IActionResult AdminPanel()
    {
        return View("~/Views/Services/admin.cshtml");
    }


}


