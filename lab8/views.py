import ast
from django.shortcuts import render
from .cipher import HashFunctions


# Create your views here.
def lab8(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "hashing_form":
            message = request.POST.get("hashing_original_message", "")

            functions = HashFunctions()
            checksum_parity = functions.checksum_parity(message)
            mid_square_hash = functions.mid_square_hash(message)
            modular_hash = functions.modular_hash(message)
            number_system_conversion = functions.number_system_conversion(message)
            folding_hash = functions.folding_hash(message)

            # Add both original and processed messages to context
            context["hashing_original_message"] = message
            context["checksum_parity"] = checksum_parity
            context["mid_square_hash"] = mid_square_hash
            context["modular_hash"] = modular_hash
            context["number_system_conversion"] = number_system_conversion
            context["folding_hash"] = folding_hash

            return render(request, "lab8.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab8.html", context)
