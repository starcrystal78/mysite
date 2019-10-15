# import here
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
)
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_code_styling(features):
    # step1
    feature_name = ""
    type_ = "CODE"
    tag = "code"

    # step 2
    control = {
        "type": type_,
        "label": "</>",
        "description": "code"
    }

    # step3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    # step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # step 6
    # this will register this features with all rich_text editor by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """ Creates centered text in out rich_text """
    feature_name = "center"
    type_ = "CENTER_TEXT"
    tag = "div"

    control = {
        "type": type_,
        "label": "center",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        }
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)

    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center"
                    }
                }
            }
        }
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)
