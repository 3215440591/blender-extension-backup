# ------------------------------------------------------------------------
# Extension Backup Utility
# ------------------------------------------------------------------------
# Author: g3215440591.gmail.com
# Version: 1.0.0
# Blender Version: 4.2.0
# Category: System
# ------------------------------------------------------------------------
# Description:
# This Blender add-on provides a utility for backing up and restoring
# official Blender extensions in JSON format. It allows users to export
# a list of installed extensions for backup or migration purposes.
#
# Supported Extensions:
# - Official extensions from Blender's extension repository
#   (https://extensions.blender.org/).
#
# License:
# This add-on is distributed under the GPL license.
# ------------------------------------------------------------------------

bl_info = {
    "name": "Extension Backup Utility",
    "author": "g3215440591.gmail.com",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Extension Backup",
    "description": "Backup or restore extensions via JSON. Currently supports official extensions only(https://extensions.blender.org/).",
    "category": "System"
}

import bpy
import json
from pathlib import Path
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import CollectionProperty, BoolProperty, StringProperty

from .i18n import _, get_language

# ---------------- Localization Helper ----------------

def get_addon_prefs():
    addon_name = __name__.split(".")[0]
    return bpy.context.preferences.addons[addon_name].preferences if addon_name in bpy.context.preferences.addons else None

# ---------------- Data Model ----------------

class OEB_AddonItem(PropertyGroup):
    name: StringProperty()
    selected: BoolProperty(default=False)
    is_installed: BoolProperty(default=False)

# ---------------- Backup Operator ----------------

class OEB_OT_BackupExtensions(Operator):
    bl_idname = "oeb.backup_extensions"
    bl_label = _("Backup Extensions(JSON)")
    bl_description = _("Export a list of installed official extensions for backup or migration.")
    filepath: StringProperty(subtype='FILE_PATH', default="blender_extensions_backup.json")
    addons_list: CollectionProperty(type=OEB_AddonItem)

    def get_official_addons(self):
        valid_addons = []
        if bpy.context.preferences and hasattr(bpy.context.preferences, 'addons'):
            for module in bpy.context.preferences.addons.keys():
                if module.startswith("bl_ext.blender_org."):
                    id_name = module.split('.')[-1]
                    valid_addons.append(id_name)
        return valid_addons

    def invoke(self, context, event):
        self.filepath = "blender_extensions_backup.json"
        self.addons_list.clear()
        installed_addons = self.get_official_addons()
        if not installed_addons:
            self.report({'WARNING'}, _("No official extensions (bl_ext.blender_org.*) found."))
        for id_name in installed_addons:
            item = self.addons_list.add()
            item.name = id_name
            item.selected = True
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        selected_ids = [item.name for item in self.addons_list if item.selected]
        if not selected_ids:
            self.report({'ERROR'}, _("No extensions selected for backup."))
            return {'CANCELLED'}

        backup_path = Path(self.filepath)
        if backup_path.is_dir():
            backup_path = backup_path / "blender_extensions_backup.json"
        elif not backup_path.suffix:
            backup_path = backup_path.with_suffix(".json")

        try:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "blender_version": bpy.app.version_string,
                    "addons": selected_ids
                }, f, indent=2, ensure_ascii=False)
            self.report({'INFO'}, _("Backup saved to: ") + str(backup_path))
        except Exception as e:
            self.report({'ERROR'}, _("Backup failed: ") + str(e))
            return {'CANCELLED'}
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if not self.addons_list:
            layout.label(text=_("No official extensions found."))
            layout.label(text=_("Or backup path not selected."))
        layout.label(text=_("Select extensions to backup:"))
        for item in self.addons_list:
            layout.prop(item, "selected", text=item.name)

# ---------------- Restore Operator ----------------

class OEB_OT_RestoreExtensions(Operator):
    bl_idname = "oeb.restore_extensions"
    bl_label = _("Restore Extensions(JSON)")
    bl_description = _("Install official extensions from a backup file, with version compatibility check.")
    bl_options = {'REGISTER'}
    filepath: StringProperty(subtype='FILE_PATH')
    addons_list: CollectionProperty(type=OEB_AddonItem)

    _parsed: BoolProperty(default=False, options={'HIDDEN'})
    _show_version_warning: BoolProperty(default=False, options={'HIDDEN'})
    _cached_backup_version: StringProperty(options={'HIDDEN'})

    def parse_backup_file_data(self):
        json_path = Path(self.filepath)
        if not json_path.exists() or not json_path.is_file():
            self.report({'ERROR'}, _("Backup file not found or invalid path: ") + self.filepath)
            return None
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    "addons": data.get("addons", []),
                    "blender_version": data.get("blender_version", "Unknown")
                }
        except json.JSONDecodeError as e:
            self.report({'ERROR'}, _("Failed to parse JSON: ") + str(e))
            return None
        except Exception as e:
            self.report({'ERROR'}, _("Failed to read backup file: ") + str(e))
            return None

    def invoke(self, context, event):
        self._parsed = False
        self._show_version_warning = False
        self._cached_backup_version = ""
        self.addons_list.clear()
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        if self._show_version_warning:
            current_blender_version = bpy.app.version_string
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(text=_("Warning: Backup file is from Blender version ") + str(self._cached_backup_version), icon='ERROR')
            row = col.row(align=True)
            row.label(text=_("Current Blender version: ") + str(current_blender_version))
            row = col.row(align=True)
            row.label(text=_("Some extensions may not be compatible. Proceed with caution."))
            layout.separator()

        if not self.addons_list and not self._parsed:
            layout.label(text=_("Please select a backup file."))
        elif not self.addons_list and self._parsed:
            layout.label(text=_("No extensions found in backup file."))
        else:
            layout.label(text=_("Select extensions to install:"))
            for item in self.addons_list:
                display_name = f"{item.name} " + (_("(Installed)") if item.is_installed else "")
                layout.prop(item, "selected", text=display_name)

    def execute(self, context):
        if not self._parsed:
            backup_info = self.parse_backup_file_data()
            if backup_info is None:
                return {'CANCELLED'}

            addons_from_file = backup_info.get("addons", [])
            self._cached_backup_version = backup_info.get("blender_version", "Unknown")
            current_blender_version = bpy.app.version_string

            self.addons_list.clear()
            if not addons_from_file:
                self.report({'WARNING'}, _("No extension information found in backup file."))

            self._show_version_warning = (self._cached_backup_version != current_blender_version)

            known_addons_modules = []
            if bpy.context.preferences and hasattr(bpy.context.preferences, 'addons'):
                known_addons_modules = bpy.context.preferences.addons.keys()

            for id_name in addons_from_file:
                module_name = "bl_ext.blender_org." + id_name
                item = self.addons_list.add()
                item.name = id_name
                addon_pref = bpy.context.preferences.addons.get(module_name)
                if addon_pref:
                    item.is_installed = True
                    item.selected = False
                else:
                    item.is_installed = False
                    item.selected = True

            self._parsed = True
            dialog_width = 450 if self._show_version_warning else 400
            return context.window_manager.invoke_props_dialog(self, width=dialog_width)
        else:
            selected_ids = [item.name for item in self.addons_list if item.selected]
            if not selected_ids:
                self.report({'WARNING'}, _("No extensions selected for installation."))
                self._parsed = False
                self._show_version_warning = False
                self._cached_backup_version = ""
                return {'CANCELLED'}

            success_count = 0
            failed_addons = []

            for id_name in selected_ids:
                try:
                    self.report({'INFO'}, _("Installing: ") + id_name)
                    bpy.ops.extensions.package_install(pkg_id=id_name, repo_index=0, enable_on_install=True)
                    success_count += 1
                    self.report({'INFO'}, _("Successfully installed and enabled: ") + id_name)
                except RuntimeError as e:
                    if "already installed and enabled" in str(e).lower() or "already enabled" in str(e).lower():
                        self.report({'WARNING'}, _("Extension already installed and enabled: ") + id_name)
                        success_count += 1
                    else:
                        self.report({'ERROR'}, _("Installation failed: ") + id_name + " - " + str(e))
                        failed_addons.append(id_name)
                except Exception as e:
                    self.report({'ERROR'}, _("Unknown error during installation: ") + id_name + " - " + str(e))
                    failed_addons.append(id_name)

            if bpy.context.preferences:
                bpy.ops.preferences.addon_refresh()
                bpy.ops.wm.save_userpref()

            if success_count > 0:
                self.report({'INFO'}, _("Successfully installed {}/{} extensions.").format(success_count, len(selected_ids)))
            if failed_addons:
                self.report({'WARNING'}, _("Failed to install the following extensions: ") + ", ".join(failed_addons))

            self._parsed = False
            self._show_version_warning = False
            self._cached_backup_version = ""
            return {'FINISHED'}

# ---------------- UI Panel ----------------

class OEB_PT_BackupPanel(Panel):
    bl_label = _("Extension Backup Utility")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = _("Extension Backup")

    def draw(self, context):
        layout = self.layout
        layout.operator(OEB_OT_BackupExtensions.bl_idname, text=_("Backup Extensions(JSON)"), icon='EXPORT')
        layout.operator(OEB_OT_RestoreExtensions.bl_idname, text=_("Restore Extensions(JSON)"), icon='IMPORT')

# ---------------- Registration ----------------

classes = (
    OEB_AddonItem,
    OEB_OT_BackupExtensions,
    OEB_OT_RestoreExtensions,
    OEB_PT_BackupPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()