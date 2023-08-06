from django.apps import AppConfig
from django.core.checks import Error, Tags, register


class CMISConfig(AppConfig):
    name = "drc_cmis"
    verbose_name = "CMIS"
    app_name = "cmis"

    def ready(self):
        # pass
        register(check_cmis, Tags.compatibility, deploy=True)


def check_cmis(app_configs, **kwargs):
    """
    ZDS 1.2.01, hoofdstuk 5:
    Ten behoeve van de integratie met het DRC en het vastleggen van
    zaakdocumenten dient het DMS aan de volgende eisen te voldoen:

        * Het DMS wordt ontsloten als een CMIS 1.0 repository;
        * De CMIS-interface dient minimaal navolgende opties te ondersteunen:
            - "Multi-filing";
            - "Change Log", met registratie van Change Events voor
              filing/unfiling/moving van de objecten documenten en folders;
            - Nieuwe CMIS-objecttypes van het Base Type "cmis:document" en
              "cmis:folder" worden ondersteund;
        * De CMIS-changelog is toegankelijk voor het DRC.

    :param app_configs:
    :param kwargs:
    :return:
    """
    from .client import cmis_client
    from .choices import CMISCapabilities

    errors = []
    try:
        capabilities = cmis_client._repo.capabilities
    except Exception:
        errors.append(
            Error(
                "Could not communicate with the DMS.",
                hint="Make sure the authentication and host settings are correct.",
            )
        )
        return errors
    else:
        multifiling = capabilities.get(CMISCapabilities.multifiling, None)
        if not multifiling:
            errors.append(Error("The DMS does not support Multifiling, or it's disabled."))
        unfiling = capabilities.get(CMISCapabilities.unfiling, None)
        if not unfiling:
            errors.append(Error("The DMS does not support Unfiling or it's disabled."))
        changes = capabilities.get(CMISCapabilities.changes, None)
        if not changes or changes == "none":
            errors.append(
                Error(
                    "The DMS does not support Change Log, or it's disabled.",
                    hint="In case you're running Alfresco, make sure to add the relevant audit.* properties.",
                )
            )

    return errors
