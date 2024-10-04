using CoffeeMachine.Models;
using CoffeeMachine.Services;
using Microsoft.AspNetCore.Mvc;

namespace CoffeeMachine.Controllers;

[ApiController]
[Route("/")]
public class CoffeeStateController : ControllerBase
{
    public CoffeeStateController()
    {
    }

    [HttpGet]
    public ActionResult<CoffeeState> GetCurrentState() =>
        CoffeeStateService.GetCurrentState();

    [HttpPost]
    public IActionResult SetCurrentState(CoffeeState state)
    {
        CoffeeStateService.SetCurrentState(state);
        return CreatedAtAction(nameof(GetCurrentState), null, state);
    }
}
