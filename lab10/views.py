import ast
from django.shortcuts import render
from .cipher import FrequencySubstitutionCipher, TranspositionCipher, ColumnarTranspositionCipher


# Create your views here.
def lab10(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "frequency_substitution_encrypt_form":
            message = request.POST.get("frequency_substitution_original_message", "")

            encrypted_message = FrequencySubstitutionCipher().encrypt(message)

            # Add both original and processed messages to context
            context["frequency_substitution_original_message"] = message
            context["frequency_substitution_encrypted_message"] = encrypted_message

            return render(request, "lab10.html", context)
        elif form_type == "frequency_substitution_decrypt_form":
            encrypted_message = request.POST.get("frequency_substitution_encrypted_message", "")

            decrypted_message = FrequencySubstitutionCipher().decrypt(encrypted_message)

            context["frequency_substitution_decrypted_message"] = decrypted_message

            return render(request, "lab10.html", context)
        elif form_type == "transposition_encrypt_form":
            message = request.POST.get("transposition_original_message", "")

            encrypted_message, metadata = TranspositionCipher().encrypt(message, [0, 5, 10])

            # Add both original and processed messages to context
            context["transposition_original_message"] = message
            context["transposition_encrypted_message"] = encrypted_message
            context["transposition_meta_data"] = metadata

            return render(request, "lab10.html", context)
        elif form_type == "transposition_decrypt_form":
            encrypted_message = request.POST.get("transposition_encrypted_message", "")
            meta_data = request.POST.get("transposition_meta_data", "")

            decrypted_message = TranspositionCipher().decrypt(encrypted_message, ast.literal_eval(meta_data))

            context["transposition_decrypted_message"] = decrypted_message

            return render(request, "lab10.html", context)

        elif form_type == "сolumnartransposition_encrypt_form":
            message = request.POST.get("сolumnartransposition_original_message", "")

            encrypted_message, key, metadata = ColumnarTranspositionCipher().encrypt(message)

            # Add both original and processed messages to context
            context["сolumnartransposition_original_message"] = message
            context["сolumnartransposition_encrypted_message"] = encrypted_message
            context["сolumnartransposition_key"] = key
            context["сolumnartransposition_meta_data"] = metadata

            return render(request, "lab10.html", context)

        elif form_type == "сolumnartransposition_decrypt_form":
            encrypted_message = request.POST.get("сolumnartransposition_encrypted_message", "")
            key = request.POST.get("сolumnartransposition_key", "")
            metadata = request.POST.get("сolumnartransposition_meta_data", "")

            decrypted_message = ColumnarTranspositionCipher().decrypt_with_key(encrypted_message, ast.literal_eval(key), ast.literal_eval(metadata))

            # Add both original and processed messages to context
            context["сolumnartransposition_decrypted_message"] = decrypted_message

            return render(request, "lab10.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab10.html", context)
