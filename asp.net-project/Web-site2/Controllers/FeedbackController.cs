using Microsoft.AspNetCore.Mvc;
using Npgsql;
using System;

namespace SalonApp.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BookingsController : Controller
    {
        private readonly string _connectionString = "Host=localhost;Port=5432;Database=BeautySite;Username=postgres;Password=nika11";

        [HttpPost("register")]
        public IActionResult RegisterClient([FromBody] ClientDto client)
        {
            using var connection = new NpgsqlConnection(_connectionString);
            connection.Open();

            string checkPhoneQuery = "SELECT COUNT(*) FROM customers WHERE phone = @phone";
            using var checkCommand = new NpgsqlCommand(checkPhoneQuery, connection);
            checkCommand.Parameters.AddWithValue("@phone", client.Phone); 

            var phoneExists = (long)checkCommand.ExecuteScalar();

            if (phoneExists > 0)
            {
                return Conflict(new { message = "Цей номер телефону вже зареєстрований." });
            }

            string insertCustomerQuery = "INSERT INTO customers (name, phone) VALUES (@name, @phone) RETURNING customer_id";
            using var command = new NpgsqlCommand(insertCustomerQuery, connection);
            command.Parameters.AddWithValue("@name", client.Name);
            command.Parameters.AddWithValue("@phone", client.Phone);

            try
            {
                var customerId = command.ExecuteScalar();
                return Ok(new { CustomerId = customerId });
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }



        [HttpPost("book")]
        public IActionResult BookAppointment([FromBody] AppointmentRequestDto appointmentRequest)
        {
            using var connection = new NpgsqlConnection(_connectionString);
            connection.Open();

            string findCustomerQuery = "SELECT customer_id FROM customers WHERE name = @name AND phone = @phone";
            using var findCommand = new NpgsqlCommand(findCustomerQuery, connection);
            findCommand.Parameters.AddWithValue("name", appointmentRequest.Name);
            findCommand.Parameters.AddWithValue("phone", appointmentRequest.Phone);

            var customerId = findCommand.ExecuteScalar();

            if (customerId == null)
            {
                return BadRequest(new { message = "Будь ласка, зареєструйтесь перед записом на послугу." });
            }

            string checkAvailabilityQuery = @"
            SELECT COUNT(*)
            FROM appointments a
            JOIN services s ON a.service = s.name
            WHERE s.category = (SELECT category FROM services WHERE name = @service)
            AND a.appointment_time = @appointmentTime";

            using var checkCommand = new NpgsqlCommand(checkAvailabilityQuery, connection);
            checkCommand.Parameters.AddWithValue("service", appointmentRequest.Service);
            checkCommand.Parameters.AddWithValue("appointmentTime", appointmentRequest.AppointmentTime);

            var slotCount = (long)checkCommand.ExecuteScalar();

            if (slotCount > 0)
            {
                return Conflict(new { message = "Цей час вже заброньовано для послуги в тій же категорії. Будь ласка, виберіть інший час." });
            }

            string insertAppointmentQuery = "INSERT INTO appointments (customer_id, service, appointment_time) VALUES (@customerId, @service, @appointmentTime)";
            using var insertCommand = new NpgsqlCommand(insertAppointmentQuery, connection);
            insertCommand.Parameters.AddWithValue("customerId", (int)customerId);
            insertCommand.Parameters.AddWithValue("service", appointmentRequest.Service);
            insertCommand.Parameters.AddWithValue("appointmentTime", appointmentRequest.AppointmentTime);

            try
            {
                insertCommand.ExecuteNonQuery();
                return Ok(new { message = "Запис успішно створено!" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }




        [HttpGet("bookedSlots")]
        public IActionResult GetBookedSlots()
        {
            using var connection = new NpgsqlConnection(_connectionString);
            connection.Open();

            string query = "SELECT appointment_time FROM appointments";
            using var command = new NpgsqlCommand(query, connection);
            using var reader = command.ExecuteReader();

            var bookedSlots = new List<DateTime>();
            while (reader.Read())
            {
                bookedSlots.Add(reader.GetDateTime(0));
            }

            return Ok(bookedSlots);
        }
        [HttpGet("services")] 
        public IActionResult GetServices([FromQuery] string category)
        {
            using var connection = new NpgsqlConnection(_connectionString);
            connection.Open();

            string query = "SELECT name FROM services WHERE category = @category";
            using var command = new NpgsqlCommand(query, connection);
            command.Parameters.AddWithValue("category", category);

            using var reader = command.ExecuteReader();
            var serviceList = new List<object>();
            while (reader.Read())
            {
                serviceList.Add(new { name = reader.GetString(0) });
            }

            return Ok(serviceList);
        }

        [HttpGet("booking/panel")]
        public IActionResult BokingPanel()
        {
            return View("~/Views/Services/booking.cshtml");
        }
    }

    public class ClientDto
    {
        public string Name { get; set; }
        public string Phone { get; set; }
    }

    public class AppointmentRequestDto
    {
        public string Name { get; set; }
        public string Phone { get; set; }
        public string Service { get; set; }
        public DateTime AppointmentTime { get; set; }
    }
}
