import ast
import json
from django.shortcuts import render
from .cipher import KnapsackCipher


# Create your views here.
def lab6(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "knapsack_encrypt_form":
            message = request.POST.get("knapsack_original_message", "")

            result = KnapsackCipher().encrypt(message)
            binary_code = result['binary_code']
            public_key = result['public_key']
            encrypted_message = result['encrypted_message']
            visualization_data = result['visualization_data']

            # Add both original and processed messages to context
            context["knapsack_original_message"] = message
            context["knapsack_binary_code"] = binary_code
            context["knapsack_public_key"] = public_key
            context["knapsack_encrypted_message"] = encrypted_message
            context["knapsack_visualization_data"] = visualization_data

            return render(request, "lab6.html", context)
        elif form_type == "knapsack_decrypt_form":
            encrypted_message = request.POST.get("knapsack_encrypted_message", "")
            public_key = request.POST.get("knapsack_public_key", "")

            decrypted_message = KnapsackCipher().decrypt(encrypted_message, ast.literal_eval(public_key))

            context["knapsack_decrypted_message"] = decrypted_message

            return render(request, "lab6.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab6.html", context)
