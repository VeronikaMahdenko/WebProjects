using System.ComponentModel.DataAnnotations;

namespace Web_site2.Models
{
    public class Service
    {
        public int Id { get; set; }

        [Required]
        public string Name { get; set; }

        [Required]
        public string Description { get; set; }

 

        public string ImageUrl { get; set; }
    }
}